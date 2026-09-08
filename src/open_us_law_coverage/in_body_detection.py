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
~3.3 GB row-group, so this scans **row-group-at-a-time** with the pool released between
groups (peak ≈ one row-group, like ``recon.py``), and a vectorised Arrow pre-filter pulls
only bodies that contain an explicit code token into Python — bare-reference bodies are
skipped by construction (they carry no ``U.S.C.``/``C.F.R.`` token), which is exactly the
population the detector abstains on.

Regenerate::

    uv run python -m open_us_law_coverage.in_body_detection \\
        data/v2026.08_full/us_federal_statutes.parquet \\
        data/v2026.08_full/us_federal_regulations.parquet \\
        --snapshot v2026.08 --out reports/M2_in_body_detection.md
"""

from __future__ import annotations

import argparse
import glob as globlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from .citation_parser import detect_mentions
from .coverage_baseline import FederalCorpus

_COLUMNS = [
    "text",
    "act_id",
    "title_number",
    "cross_references_usc",
    "cross_references_cfr",
]

# A superset (RE2) of everything the detector can match: an explicit code token. A body
# that lacks all of these cannot contain an explicit citation, so it is skipped before any
# Python regex runs — and that skipped population is precisely the bare/relative references
# the explicit detector abstains on.
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
    # Small sorted samples of detector-only edges (explicit cites the dataset did not list).
    usc_detector_only_ex: set[tuple[str, str, str]] = field(default_factory=set)


_EXAMPLE_CAP = 40


def scan_file(path: str | Path) -> InBodyStats:
    path = Path(path)
    stats = InBodyStats(corpus_file=path.name.replace(".parquet", ""))
    pf = pq.ParquetFile(path)
    pool = pa.default_memory_pool()

    for g in range(pf.metadata.num_row_groups):
        tbl = pf.read_row_group(g, columns=_COLUMNS)
        text_col = tbl.column("text")
        # Coarse filter: valid text that contains an explicit code token. Nulls -> False.
        mask = pc.and_(
            pc.is_valid(text_col), pc.match_substring_regex(text_col, _CANDIDATE_RE)
        ).to_pylist()
        titles = tbl.column("title_number").to_pylist()
        xusc = tbl.column("cross_references_usc").to_pylist()
        xcfr = tbl.column("cross_references_cfr").to_pylist()

        for i in range(tbl.num_rows):
            stats.rows_total += 1
            ds_usc = _parse_xref_usc(xusc[i], titles[i])
            ds_cfr = _parse_xref_cfr(xcfr[i], titles[i])

            det_usc: set[_Cite] = set()
            det_cfr: set[_Cite] = set()
            if mask[i]:
                stats.rows_candidate += 1
                mentions = detect_mentions(text_col[i].as_py())  # one body only
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

            stats.usc_both += len(det_usc & ds_usc)
            stats.usc_detector_only += len(det_usc - ds_usc)
            stats.usc_dataset_only += len(ds_usc - det_usc)
            stats.cfr_both += len(det_cfr & ds_cfr)
            stats.cfr_detector_only += len(det_cfr - ds_cfr)
            stats.cfr_dataset_only += len(ds_cfr - det_cfr)
            if len(stats.usc_detector_only_ex) < _EXAMPLE_CAP:
                for t, s in sorted(det_usc - ds_usc):
                    stats.usc_detector_only_ex.add(("usc", t, s))

        del tbl, text_col
        pool.release_unused()
    return stats


def _pct(numer: int, denom: int) -> str:
    return f"{100.0 * numer / denom:.2f}%" if denom else "—"


def render_report(stats_list: list[InBodyStats], snapshot: str) -> str:
    lines: list[str] = []
    A = lines.append
    A("# M2 corpus-scale in-body citation detection")
    A("")
    A(f"Snapshot: `{snapshot}`. The Stage-A exact-citation detector (`detect_mentions`) run")
    A("over **every row body** in each file, row-group-bounded (never materialising the 11 GB")
    A("regulations `text` column). A vectorised Arrow pre-filter Python-scans only bodies that")
    A("carry an explicit code token; the rest cannot contain an explicit citation.")
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
    all_ex = sorted({e for st in stats_list for e in st.usc_detector_only_ex})[:20]
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
        "the whole text column (row-group-bounded) and compare with cross_references."
    )
    ap.add_argument("paths", nargs="+", help="Parquet file(s) or glob(s)")
    ap.add_argument("--snapshot", required=True, help="snapshot version, e.g. v2026.08")
    ap.add_argument("--out", help="write the Markdown report here (else stdout)")
    args = ap.parse_args(argv)

    files = sorted({Path(p) for pat in args.paths for p in globlib.glob(pat)})
    stats_list = [scan_file(f) for f in files]
    report = render_report(stats_list, args.snapshot)
    if args.out:
        Path(args.out).write_text(report)
        print(f"wrote {args.out} ({len(files)} files)")
    else:
        print(report)


if __name__ == "__main__":
    main()
