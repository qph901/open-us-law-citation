"""Snapshot text-integrity audit — is the text in a row actually the whole provision?

A supporting audit, **not a chartered milestone**. It exists because `PRIORITIES.md` puts
measurable law coverage first, and a row that is *present* but whose text is truncated or
padded with website chrome is not coverage: the crosswalk would score it `represented`
while the operative text is incomplete. Structural presence and textual integrity are
different claims, and only the first has been measured so far.

Every defect class here was found by inspection during other work and is then measured
corpus-wide, never the other way round:

* **truncated head** — the body begins mid-word. Real examples: `'ited States or any
  State…'` (`United` lost), `'ublic health, safety…'`, `'piled by a criminal law
  enforcement authority…'` (`compiled`), `'ewed Amendment Number 4…'` (`Renewed`). The
  detector is deliberately blunt — the first non-space character is a lowercase letter —
  and the report samples it so the rate can be read with the proxy's coarseness in view.
* **UI chrome** — the body carries the eCFR banner `Link to an amendment published…`,
  which is website furniture captured as legal text.
* **impossible-title citation** — a digit run adjacent to a code token immediately after a
  newline (`\\n0 CFR 264.100`, really 40 CFR 264.100). The same damage that made M2's
  impossible-title guard necessary; see `reports/M2_in_body_detection.md`.
* **corrupt cross-reference** — the dataset's own `cross_references_usc` naming a US Code
  title that does not exist (1-54), i.e. the damage propagating out of the text into the
  extracted fields.

Memory: aggregates run in DuckDB under a hard ``--memory-limit`` with disk spill, so the
~11 GB regulations ``text`` column streams and never materialises a row-group (CLAUDE.md).
Samples are pulled with a bounded ``LIMIT`` and truncated in SQL.

Regenerate::

    uv run python -m open_us_law_citation.text_integrity \\
        data/v2026.08_full/us_federal_statutes.parquet \\
        data/v2026.08_full/us_federal_regulations.parquet \\
        --snapshot v2026.08 --out reports/snapshot_text_integrity.md \\
        --memory-limit 3GB --temp-dir /path/to/scratch/ddspill
"""

from __future__ import annotations

import argparse
import glob as globlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import duckdb

# RE2, evaluated inside DuckDB.
_LOWER_START = r"^[a-z]"
_ECFR_BANNER = "Link to an amendment published"
# A digit run adjacent to a code token that no title can have: a leading zero, or three or
# more digits (USC stops at 54, CFR at 50). Two damage shapes produce it, in opposite
# orders, so the detector is deliberately shape-agnostic rather than anchored to a newline:
#   * the leading digit is lost at a line break -- "Implementation\n0 CFR 264.100" (40 CFR);
#   * a flattened table's column bleeds into the citation -- "January 3, 2023\nCFR 2.2"
#     (50 CFR), or "$122,661\nU.S.C. 362(a)" (47 U.S.C.).
# A citation that merely happens to begin a line ("\n42 U.S.C. 1983") is ordinary text and
# must not count; requiring an impossible title is what separates the two.
_IMPOSSIBLE_TITLE_CITE = (
    r"(^|[^0-9])(0[0-9]*|[0-9]{3,})\s*(U\.?\s?S\.?\s?C|C\.?\s?F\.?\s?R)"
)

_SAMPLE_LIMIT = 8
_SAMPLE_CHARS = 88


@dataclass
class FileIntegrity:
    corpus_file: str
    rows: int = 0
    non_null_text: int = 0
    truncated_head: int = 0
    ui_chrome: int = 0
    impossible_title_cites: int = 0
    corrupt_xref_titles: int = 0
    truncated_examples: list[tuple[str, str]] = field(default_factory=list)
    chrome_examples: list[tuple[str, str]] = field(default_factory=list)


def _connect(memory_limit: str, temp_dir: Path | None) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute(f"SET memory_limit='{memory_limit}'")
    if temp_dir is not None:
        temp_dir.mkdir(parents=True, exist_ok=True)
        con.execute(f"SET temp_directory='{temp_dir.as_posix()}'")
    con.execute("SET threads=1")
    con.execute("SET preserve_insertion_order=false")
    return con


_COUNTS_SQL = """
SELECT COUNT(*),
       COUNT(*) FILTER (WHERE text IS NOT NULL),
       COUNT(*) FILTER (WHERE text IS NOT NULL AND regexp_matches(trim(text), ?)),
       COUNT(*) FILTER (WHERE text LIKE ?),
       COUNT(*) FILTER (WHERE text IS NOT NULL AND regexp_matches(text, ?))
FROM read_parquet(?)
"""

# A cross-reference entry is "title:section"; the title is the part before the colon.
# USC has 54 titles, so anything outside 1-54 cannot name real law.
_XREF_SQL = """
SELECT COUNT(*) FROM read_parquet(?)
WHERE cross_references_usc IS NOT NULL AND cross_references_usc <> '[]'
  AND regexp_matches(cross_references_usc, '"(0|5[5-9]|[6-9][0-9]|[1-9][0-9]{2,}):')
"""

_SAMPLE_SQL = """
SELECT act_id, left(trim(text), {chars})
FROM read_parquet(?)
WHERE text IS NOT NULL AND {predicate}
ORDER BY act_id
LIMIT {limit}
"""


def scan_file(
    path: str | Path,
    *,
    memory_limit: str = "3GB",
    temp_dir: Path | None = None,
) -> FileIntegrity:
    path = Path(path)
    p = path.as_posix()
    con = _connect(memory_limit, temp_dir)
    try:
        counts = con.execute(
            _COUNTS_SQL, [_LOWER_START, f"%{_ECFR_BANNER}%", _IMPOSSIBLE_TITLE_CITE, p]
        ).fetchone() or (0, 0, 0, 0, 0)
        xref = (con.execute(_XREF_SQL, [p]).fetchone() or (0,))[0]
        trunc = con.execute(
            # Same rule as the count above: one definition, not a second literal that
            # happens to agree — a sample that disagreed with its own count is worse than
            # no sample.
            _SAMPLE_SQL.format(chars=_SAMPLE_CHARS, limit=_SAMPLE_LIMIT,
                               predicate=f"regexp_matches(trim(text), '{_LOWER_START}')"),
            [p],
        ).fetchall()
        chrome = con.execute(
            _SAMPLE_SQL.format(chars=_SAMPLE_CHARS, limit=_SAMPLE_LIMIT,
                               predicate=f"text LIKE '%{_ECFR_BANNER}%'"),
            [p],
        ).fetchall()
    finally:
        con.close()
    return FileIntegrity(
        corpus_file=path.name.replace(".parquet", ""),
        rows=int(counts[0]), non_null_text=int(counts[1]),
        truncated_head=int(counts[2]), ui_chrome=int(counts[3]),
        impossible_title_cites=int(counts[4]), corrupt_xref_titles=int(xref),
        truncated_examples=[(a, t) for a, t in trunc],
        chrome_examples=[(a, t) for a, t in chrome],
    )


_EXIT_SECTION = """\
## Why this is a coverage question, not a tidiness question

COV-1A scores a provision `represented` when exactly one dataset row sits at the official
key. That test is **structural**: it asks whether a row exists, never whether the row holds
the whole provision. A truncated body passes it. So the represented rate and the truncation
rate are independent, and a coverage number quoted without the second is an overstatement of
what the corpus can actually answer with.

Text agreement (COV-1A's third dimension) would catch these — but only once the official
oracle is staged and only where the comparison is not `pending`. This audit needs no oracle
at all, so it is available now and stays available for every corpus that has no oracle.

## What the truncation signal is, and is not

The detector is deliberately blunt: the first non-space character of the body is a lowercase
letter. Sampled, it is overwhelmingly genuine mid-word truncation — `'ited States or any
State…'`, `'ublic health, safety, or interest…'`, `'piled by a criminal law enforcement
authority…'`, `'ewed Amendment Number 4…'` — but it is a proxy, not a proof, and a body that
legitimately opens on a lowercase word would be counted. Read the rate with that in view;
the samples below are provided so it can be judged rather than taken on trust.

The converse error is invisible here: a body truncated at a **word boundary** ("United
States or any State…" with an earlier paragraph missing) reads as a clean start and is not
counted. **The measured rate is therefore a lower bound on truncation.**

## Cross-check against CFR-A1

Several `act_id`s counted here as truncated are ones `reports/CFR-A1_commissioning_frame.md`
classified `candidate_segmented` — the stratum whose rows show a mid-thought continuation
seam. That overlap matters for CFR-A2: a "continuation" seam between two rows is equally
consistent with **one row being a truncated capture** as with the two being ordered segments
of one section. It is further evidence for the selection-over-composition respecification —
concatenating a truncated capture to its sibling does not reconstruct the section, it
splices across a hole — and it means the 31 `candidate_segmented` groups need the eCFR
comparison before any of them is treated as composable.
"""


def _pct(numer: int, denom: int) -> str:
    return f"{100.0 * numer / denom:.2f}%" if denom else "—"


def render_report(files: list[FileIntegrity], snapshot: str) -> str:
    lines: list[str] = []
    A = lines.append
    A("# Snapshot text integrity")
    A("")
    A(f"Snapshot: `{snapshot}`. Does a row's `text` hold the whole provision? A supporting")
    A("audit, not a chartered milestone, and one that needs **no official oracle** — every")
    A("defect below is detectable from the snapshot alone.")
    A("")
    A("## Defect rates")
    A("")
    A("| file | rows | non-null text | truncated head | UI chrome | impossible-title citation |")
    A("|---|---:|---:|---:|---:|---:|")
    for f in files:
        A(f"| {f.corpus_file} | {f.rows:,} | {f.non_null_text:,} | "
          f"{f.truncated_head:,} ({_pct(f.truncated_head, f.non_null_text)}) | "
          f"{f.ui_chrome:,} | {f.impossible_title_cites:,} |")
    A("")
    A("`truncated head` = the body begins with a lowercase letter, i.e. mid-word. "
      "`UI chrome` = the body carries the eCFR banner `Link to an amendment published…`, "
      "website furniture captured as legal text. `impossible-title citation` = a digit run "
      "adjacent to a code token straight after a newline (`\\n0 CFR 264.100`, really 40 CFR).")
    A("")
    A("## Damage that reached the extracted fields")
    A("")
    A("Rows whose own `cross_references_usc` names a US Code title that does not exist "
      "(outside 1-54) — the corruption propagating out of the text into the dataset's "
      "structured columns.")
    A("")
    A("| file | rows with an impossible cross-reference title |")
    A("|---|---:|")
    for f in files:
        A(f"| {f.corpus_file} | {f.corrupt_xref_titles:,} |")
    A("")
    for f in files:
        if not f.truncated_examples and not f.chrome_examples:
            continue
        A(f"## Samples — {f.corpus_file}")
        A("")
        if f.truncated_examples:
            A("Truncated heads (each begins mid-word):")
            A("")
            for act_id, head in f.truncated_examples:
                A(f"- `{act_id}` — `{head}…`")
            A("")
        if f.chrome_examples:
            A("UI chrome in the body:")
            A("")
            for act_id, head in f.chrome_examples:
                A(f"- `{act_id}` — `{head}…`")
            A("")
    A(_EXIT_SECTION)
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description="Snapshot text-integrity audit — truncated bodies, captured UI chrome, "
        "and corruption that reached the extracted cross-reference fields."
    )
    ap.add_argument("paths", nargs="+", help="Parquet file(s) or glob(s)")
    ap.add_argument("--snapshot", required=True, help="snapshot version, e.g. v2026.08")
    ap.add_argument("--out", help="write the Markdown report here (else stdout)")
    ap.add_argument("--memory-limit", default="3GB",
                    help="DuckDB hard memory limit (spills to --temp-dir beyond this).")
    ap.add_argument("--temp-dir", type=Path, default=Path(".duckdb_spill"),
                    help="scratch directory for DuckDB spill files.")
    args = ap.parse_args(argv)

    paths = sorted({Path(p) for pat in args.paths for p in globlib.glob(pat)})
    files = []
    for path in paths:
        print(f"scanning {path.name} ...", flush=True)
        files.append(scan_file(path, memory_limit=args.memory_limit, temp_dir=args.temp_dir))
    report = render_report(files, args.snapshot)
    if args.out:
        Path(args.out).write_text(report)
        print(f"wrote {args.out} ({len(files)} files)")
    else:
        print(report)


if __name__ == "__main__":
    main()
