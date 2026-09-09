"""M2 (corpus-scale) — run the exact-citation detector over the whole ``text`` column.

The Stage-A gold set measures the detector on curated passages; this harness runs the same
`detect_mentions` over **every row's body** in a corpus and reports what explicit-citation
detection covers at scale, plus its agreement with the dataset's own pre-extracted
``cross_references_usc`` / ``cross_references_cfr``.

**This is the M2/M4 boundary made measurable, not a recall gate.** M2 detects *explicit*
citations (``42 U.S.C. § 1983``, ``section 552 of title 5, United States Code``). The
dataset's in-body cross-references are dominated by **bare, context-relative** references
(``§ 4.1045`` — same-title, no code token), which are LOCAL/RELATIVE resolution and belong
to the hierarchy resolver / M4, and which the explicit detector correctly does **not** fire
on. So "dataset-only" is expected and large (especially for CFR); it is not a detector
miss. And per PROPOSAL.md, ``cross_references_*`` field presence "is not a recall floor" —
it is an independent comparison signal, never a gold denominator.

OOM invariant (CLAUDE.md): the federal-regulations ``text`` column is ~11 GB with a single
~3.3 GB row-group. The pyarrow ``read_row_group`` pattern that ``recon.py`` uses materialises
that whole row-group and **SIGKILLs a 14 GB box** on this file (measured: exit 137). Per the
CLAUDE.md corollary, all ``text`` work here therefore runs in **DuckDB** under a hard
``--memory-limit`` with disk spill to ``--temp-dir``: it streams the column in vectors, never
holding a row-group.

Two things keep the streamed footprint small. The coarse code-token pre-filter is **pushed
into SQL** (``regexp_matches``), and a non-candidate body is projected to ``NULL`` — so bodies
that cannot contain an explicit citation are never returned to Python at all, and the peak is
one record batch of *candidate* bodies (``--rows-per-batch``), not one row-group. Skipping
them is not a shortcut: a body with no code token is precisely the bare/relative population
the explicit detector abstains on.

Determinism: every reported number is an order-independent aggregate, and the example sample
is the lexicographically smallest N edges rather than the first N encountered — so the report
is byte-stable under any scan order, thread count, or batch size.

Regenerate::

    uv run python -m open_us_law_citation.in_body_detection \\
        data/v2026.08_full/us_federal_statutes.parquet \\
        data/v2026.08_full/us_federal_regulations.parquet \\
        --snapshot v2026.08 --out reports/M2_in_body_detection.md \\
        --memory-limit 2GB --temp-dir /path/to/scratch/ddspill
"""

from __future__ import annotations

import argparse
import glob as globlib
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import duckdb

from .citation_parser import detect_mentions, title_in_range
from .coverage_baseline import FederalCorpus

# A superset (RE2) of everything the detector can match: an explicit code token. A body
# that lacks all of these cannot contain an explicit citation, so it is skipped before any
# Python regex runs — and that skipped population is precisely the bare/relative references
# the explicit detector abstains on. DuckDB's ``regexp_matches`` is RE2, so this is the same
# dialect the pyarrow ``match_substring_regex`` pre-filter used.
_CANDIDATE_RE = r"U\.?\s?S\.?\s?C|C\.?\s?F\.?\s?R|United States Code|Code of Federal Regulations"

_Cite = tuple[str, str]  # (title, section)


def _coerce_xref(item: object, row_title: int | None) -> _Cite | None:
    """One cross-reference element → ``(title, section)`` or ``None``.

    The dataset stores heterogeneous shapes: ``"title:section"`` strings, **bare** strings
    (``"210.1."`` — same-title, trailing dot possible), and **part-level dicts**
    (``{"title": 40, "part": "52"}`` — a whole-part reference, not a section). Part-level
    refs are a coarser granularity than an explicit section citation, so they return
    ``None`` and stay out of the section-level comparison (they are M4 population, like the
    bare/relative refs).
    """
    if isinstance(item, str):
        item = item.strip().rstrip(".")
        if not item:
            return None
        if ":" in item:
            title, section = item.split(":", 1)
            return (title.strip(), section.strip())
        return (str(row_title), item) if row_title is not None else None
    if isinstance(item, dict):
        title, section = item.get("title"), item.get("section")
        if title is not None and section is not None:
            return (str(title).strip(), str(section).strip())
        return None  # part-only or malformed: not a section-level edge
    return None


def _parse_xrefs(raw: str | None, row_title: int | None) -> set[_Cite]:
    if not raw or raw == "[]":
        return set()
    out: set[_Cite] = set()
    for item in json.loads(raw):
        edge = _coerce_xref(item, row_title)
        if edge is not None:
            out.add(edge)
    return out


def _parse_xref_usc(raw: str | None, row_title: int | None = None) -> set[_Cite]:
    return _parse_xrefs(raw, row_title)


def _parse_xref_cfr(raw: str | None, row_title: int | None) -> set[_Cite]:
    return _parse_xrefs(raw, row_title)


@dataclass
class InBodyStats:
    corpus_file: str
    rows_total: int = 0
    rows_candidate: int = 0        # passed the coarse code-token filter
    rows_with_detection: int = 0
    usc_mentions: int = 0          # total detected (not de-duplicated)
    cfr_mentions: int = 0
    # Agreement with the dataset's cross-references, de-duplicated per row (set algebra).
    usc_both: int = 0
    usc_detector_only: int = 0
    usc_dataset_only: int = 0
    cfr_both: int = 0
    cfr_detector_only: int = 0
    cfr_dataset_only: int = 0
    # Precision tripwire: a detected edge whose title cannot exist (USC has titles 1-54,
    # CFR 1-50). These are false positives by construction — see _PRECISION_SECTION.
    usc_out_of_range: int = 0
    cfr_out_of_range: int = 0
    out_of_range_ex: set[tuple[str, str, str]] = field(default_factory=set)
    # Small sorted samples of detector-only edges (explicit cites the dataset did not list).
    usc_detector_only_ex: set[tuple[str, str, str]] = field(default_factory=set)


_EXAMPLE_CAP = 40

# The grammar now refuses to emit a citation whose title is outside its code's range
# (``title_in_range``), so this counter is a **regression guard**: it must read zero. It is
# kept rather than deleted because it is denominator-free — it needs no labelled set — and
# a non-zero value means the guard regressed or a new construction path bypassed it.
_in_range = title_in_range


_PRECISION_SECTION = """\
## Precision limits found at corpus scale

The Stage-A gold set (36 hand-labelled passages) measures precision 1.000, but it is small
by construction. Running the same detector over every federal body surfaced two defect
classes it did not cover. Both are now fixed; both are recorded here because the counts
above are only meaningful alongside what they used to be.

**1. List members folded their subsection into the section.** `47 U.S.C. §§ 154(i), 4(i)`
emitted the continuation items as section `4(i)` while the *primary* form of the same
citation splits to section `4` + subsection `(i)`, so one provision produced two different
edges. `_USC_LIST_SPLIT` now splits list members exactly like primaries (CFR is deliberately
not split — there parenthesised material is part of the section identity). That removed 654
spurious USC edges from the regulations corpus.

**2. A greedy title absorbed whatever digits were adjacent.** `(?P<title>\\d+)` accepts any
digit run, and at corpus scale the snapshot's text supplies many that are not titles. Tracing
the population found a single mechanism behind all of them, with the wrong digits arriving
from four different directions:

| Source of the digits | Example found in the corpus | Real citation |
|---|---|---|
| Leading digit dropped at a line break | `Implementation\\n0 CFR 264.100` | 40 CFR 264.100 |
| Flattened table cell (dollar column) | `$2,453,218.\\n$122,661\\nU.S.C. 362(a)` | 47 U.S.C. 362(a) |
| Flattened table cell (date column) | `on January 3, 2023\\nCFR 2.2` | 50 CFR 2.2 |
| A neighbouring number run together | `Pub. L. 95-147 U.S.C. 19` | (none — not a citation) |

The fix is `title_in_range`: the US Code has 54 titles and the CFR has 50, so a citation
naming a title outside its code's range cannot refer to real law and the grammar abstains.
It is enforced both at the parse boundary and as a `ParsedCitation` model invariant, so no
producer can route around it. Repairing such a citation was never an option — the missing
digit is not recoverable from the text, so it would mean inventing one.

**The tripwire table above is therefore a regression guard, and must read zero.** It is kept
rather than deleted because it needs no labelled set: a non-zero value means the guard
regressed or a new construction path bypassed it.

**A named sub-class: U.S. Reports citations wearing a `C`.** Three of the traced cases are
Supreme Court citations that the snapshot's text renders with a spurious `C` — `73 U.S.C.
499`, `381 U.S.C. 139 (1965)`, `479 U.S.C. 238 (1986)`, which are *U.S. Reports* volumes,
not US Code titles. The first is verifiable on its face: `us_federal_statutes` row
`USC_T28_C115_S1733` reads `Gardner v. Barney, 1867, 6 Wall. 499, 73 U.S.C. 499`, and
`6 Wall. 499` is the parallel citation for 73 U.S. 499. Notably the **dataset's own
`cross_references_usc` repeats the error** on that row (`"73:499"`), which is why the
statutes `both` count falls by one here: before the guard, detector and dataset agreed on a
citation to a title that does not exist. The corruption is upstream of both, and it
propagates out of the text into the dataset's extracted fields.

**What this does not fix.** The guard only catches titles that land *outside* the range.
The same text damage can just as easily yield an in-range wrong title — a dropped digit
turning 42 into 2 — and nothing here detects that. U.S. Reports volumes 1-54 are the
concrete case: `54 U.S.C. 498` would pass silently. The pre-fix count (657 impossible titles
across the two federal files) is a **lower bound** on this defect class, not its size. The
underlying cause is upstream: the snapshot's text loses characters at line breaks and
flattens multi-column tables into prose. That is a dataset-quality finding for the coverage
track, not something the grammar can repair.
"""


def _sample_key(edge: tuple[str, str, str]) -> str:
    """Deterministic pseudo-random order for example sampling (stable across runs)."""
    return hashlib.sha256("\x1f".join(edge).encode("utf-8")).hexdigest()


def _display_key(edge: tuple[str, str, str]) -> tuple[str, int, str, str]:
    """Human ordering for the rendered sample: numeric title, then section."""
    _, title, section = edge
    return (edge[0], int(title) if title.isdigit() else 1 << 30, title, section)

# Only the coarse-filtered ``body`` is expensive; the other three columns are tiny. A
# non-candidate body is projected to NULL, so it costs nothing to carry the row (we still
# need its cross-references for the dataset-only count).
_SCAN_SQL = """
SELECT title_number,
       cross_references_usc,
       cross_references_cfr,
       CASE WHEN text IS NOT NULL AND regexp_matches(text, ?) THEN text END AS body
FROM read_parquet(?)
"""


def _connect(memory_limit: str, temp_dir: Path | None) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute(f"SET memory_limit='{memory_limit}'")
    if temp_dir is not None:
        temp_dir.mkdir(parents=True, exist_ok=True)
        con.execute(f"SET temp_directory='{temp_dir.as_posix()}'")
    # Single-threaded, and insertion order NOT preserved: on the regulations file the
    # order-preserving buffer holds ~1.5 GiB of decoded bodies and the scan then fails to
    # allocate a 512 MiB string vector. Report stability does not depend on scan order —
    # every reported number is an order-independent aggregate and the example sample is the
    # lexicographically smallest N edges (see ``_accumulate``), not the first N seen.
    con.execute("SET threads=1")
    con.execute("SET preserve_insertion_order=false")
    return con


def _accumulate(stats: InBodyStats, body: str | None, title: int | None,
                raw_usc: str | None, raw_cfr: str | None) -> None:
    """Fold one row into ``stats``. ``body`` is None for a non-candidate row."""
    stats.rows_total += 1
    ds_usc = _parse_xref_usc(raw_usc, title)
    ds_cfr = _parse_xref_cfr(raw_cfr, title)

    det_usc: set[_Cite] = set()
    det_cfr: set[_Cite] = set()
    if body is not None:
        stats.rows_candidate += 1
        mentions = detect_mentions(body)
        if mentions:
            stats.rows_with_detection += 1
        for m in mentions:
            key = (m.parsed.parsed_title, m.parsed.parsed_section)
            if m.parsed.parsed_corpus == FederalCorpus.USC:
                det_usc.add(key)
                stats.usc_mentions += 1
            else:
                det_cfr.add(key)
                stats.cfr_mentions += 1

    for corpus, edges, attr in (
        (FederalCorpus.USC, det_usc, "usc"), (FederalCorpus.CFR, det_cfr, "cfr")
    ):
        bad = {(t, sec) for t, sec in edges if not _in_range(corpus, t)}
        if bad:
            setattr(stats, f"{attr}_out_of_range",
                    getattr(stats, f"{attr}_out_of_range") + len(bad))
            stats.out_of_range_ex.update((str(corpus), t, sec) for t, sec in bad)
            if len(stats.out_of_range_ex) > _EXAMPLE_CAP:
                stats.out_of_range_ex = set(
                    sorted(stats.out_of_range_ex, key=_sample_key)[:_EXAMPLE_CAP]
                )

    stats.usc_both += len(det_usc & ds_usc)
    stats.usc_detector_only += len(det_usc - ds_usc)
    stats.usc_dataset_only += len(ds_usc - det_usc)
    stats.cfr_both += len(det_cfr & ds_cfr)
    stats.cfr_detector_only += len(det_cfr - ds_cfr)
    stats.cfr_dataset_only += len(ds_cfr - det_cfr)
    # Order-independent sample: keep the _EXAMPLE_CAP edges with the smallest digest. This
    # is byte-stable under any scan order / threading / batch size (unlike "first N seen")
    # *and* unbiased (unlike "lexicographically smallest N", which only ever shows title 1).
    new_edges = det_usc - ds_usc
    if new_edges:
        stats.usc_detector_only_ex.update(("usc", t, sec) for t, sec in new_edges)
        if len(stats.usc_detector_only_ex) > _EXAMPLE_CAP:
            stats.usc_detector_only_ex = set(
                sorted(stats.usc_detector_only_ex, key=_sample_key)[:_EXAMPLE_CAP]
            )


def scan_file(
    path: str | Path,
    *,
    memory_limit: str = "2GB",
    temp_dir: Path | None = None,
    rows_per_batch: int = 512,
) -> InBodyStats:
    """Stream one corpus file through the detector under a hard DuckDB memory limit.

    Never materialises a Parquet row-group: DuckDB streams ``text`` in vectors and this
    pulls one Arrow record batch of *candidate* bodies at a time. Pass ``temp_dir`` for any
    large file — without a spill directory DuckDB cannot honour ``memory_limit`` on a
    query that needs to spill (the CLI always passes one).
    """
    path = Path(path)
    stats = InBodyStats(corpus_file=path.name.replace(".parquet", ""))
    con = _connect(memory_limit, temp_dir)
    try:
        reader = con.execute(
            _SCAN_SQL, [_CANDIDATE_RE, path.as_posix()]
        ).to_arrow_reader(rows_per_batch)
        for batch in reader:
            titles = batch.column("title_number").to_pylist()
            xusc = batch.column("cross_references_usc").to_pylist()
            xcfr = batch.column("cross_references_cfr").to_pylist()
            bodies = batch.column("body")
            for i in range(batch.num_rows):
                # Pull the (potentially large) body only for candidate rows.
                body = bodies[i].as_py() if bodies[i].is_valid else None
                _accumulate(stats, body, titles[i], xusc[i], xcfr[i])
            del batch, bodies
    finally:
        con.close()
    return stats


def _pct(numer: int, denom: int) -> str:
    return f"{100.0 * numer / denom:.2f}%" if denom else "—"


def render_report(stats_list: list[InBodyStats], snapshot: str) -> str:
    lines: list[str] = []
    A = lines.append
    A("# M2 corpus-scale in-body citation detection")
    A("")
    A(f"Snapshot: `{snapshot}`. The Stage-A exact-citation detector (`detect_mentions`) run")
    A("over **every row body** in each file. The scan streams through DuckDB under a hard")
    A("memory limit with disk spill, so the 11 GB regulations `text` column is never")
    A("materialised a row-group at a time (which SIGKILLs a 14 GB box). The coarse code-token")
    A("pre-filter is pushed into SQL: only bodies carrying an explicit code token are returned")
    A("to Python at all; the rest cannot contain an explicit citation.")
    A("")
    A("**This is the M2/M4 boundary, not a recall gate.** M2 detects *explicit* citations; the")
    A("dataset's `cross_references_*` are dominated by **bare, same-title** in-body references")
    A("(`§ 4.1045`) that are LOCAL/RELATIVE resolution (hierarchy / M4) and that the explicit")
    A("detector correctly does not fire on — so `dataset-only` is expected, especially for CFR,")
    A("and is never a detector miss. Field presence is a comparison signal, not a recall floor.")
    A("")
    A("## Detection volume")
    A("")
    A("| File | Rows | Candidate bodies | With detection | USC mentions | CFR mentions |")
    A("|---|---:|---:|---:|---:|---:|")
    for st in stats_list:
        A(f"| {st.corpus_file} | {st.rows_total:,} | {st.rows_candidate:,} "
          f"({_pct(st.rows_candidate, st.rows_total)}) | {st.rows_with_detection:,} "
          f"| {st.usc_mentions:,} | {st.cfr_mentions:,} |")
    A("")
    A("## Agreement with the dataset's cross-references (de-duplicated edges)")
    A("")
    A("`both` = the explicit edge is in both; `detector-only` = an explicit citation the")
    A("dataset did not list; `dataset-only` = a cross-reference the detector did not emit")
    A("(overwhelmingly bare/relative refs — the M4 population).")
    A("")
    A("| File | Corpus | both | detector-only | dataset-only |")
    A("|---|---|---:|---:|---:|")
    for st in stats_list:
        A(f"| {st.corpus_file} | USC | {st.usc_both:,} | {st.usc_detector_only:,} "
          f"| {st.usc_dataset_only:,} |")
        A(f"| {st.corpus_file} | CFR | {st.cfr_both:,} | {st.cfr_detector_only:,} "
          f"| {st.cfr_dataset_only:,} |")
    A("")
    A("## Impossible-title detections (precision tripwire)")
    A("")
    A("Distinct detected edges whose title is outside its code's range — false positives by")
    A("construction, needing no labelled set. See the section below for the cause.")
    A("")
    A("| File | USC out-of-range | CFR out-of-range |")
    A("|---|---:|---:|")
    for st in stats_list:
        A(f"| {st.corpus_file} | {st.usc_out_of_range:,} | {st.cfr_out_of_range:,} |")
    A("")
    bad_ex = sorted(
        sorted({e for st in stats_list for e in st.out_of_range_ex}, key=_sample_key)[:10],
        key=_display_key,
    )
    if bad_ex:
        A("Examples:")
        A("")
        for corpus, t, sec in bad_ex:
            A(f"- `{t} {'U.S.C.' if corpus == 'usc' else 'C.F.R.'} § {sec}`")
        A("")
    A(_PRECISION_SECTION)
    pooled = {e for st in stats_list for e in st.usc_detector_only_ex}
    all_ex = sorted(sorted(pooled, key=_sample_key)[:20], key=_display_key)
    if all_ex:
        A("## Detector-only USC edges (sample) — explicit cross-title cites in bodies")
        A("")
        for corpus, t, s in all_ex:
            A(f"- `{t} U.S.C. § {s}`")
        A("")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description="M2 corpus-scale in-body detection — run the exact-citation detector over "
        "the whole text column (DuckDB-streamed) and compare with cross_references."
    )
    ap.add_argument("paths", nargs="+", help="Parquet file(s) or glob(s)")
    ap.add_argument("--snapshot", required=True, help="snapshot version, e.g. v2026.08")
    ap.add_argument("--out", help="write the Markdown report here (else stdout)")
    ap.add_argument("--memory-limit", default="2GB",
                    help="DuckDB hard memory limit (spills to --temp-dir beyond this).")
    ap.add_argument("--temp-dir", type=Path, default=Path(".duckdb_spill"),
                    help="scratch directory for DuckDB spill files.")
    ap.add_argument("--rows-per-batch", type=int, default=512,
                    help="rows per streamed Arrow batch; lower it if bodies are very large.")
    args = ap.parse_args(argv)

    files = sorted({Path(p) for pat in args.paths for p in globlib.glob(pat)})
    stats_list = []
    for f in files:
        print(f"scanning {f.name} ...", flush=True)
        stats_list.append(
            scan_file(
                f,
                memory_limit=args.memory_limit,
                temp_dir=args.temp_dir,
                rows_per_batch=args.rows_per_batch,
            )
        )
    report = render_report(stats_list, args.snapshot)
    if args.out:
        Path(args.out).write_text(report)
        print(f"wrote {args.out} ({len(files)} files)")
    else:
        print(report)


if __name__ == "__main__":
    main()
