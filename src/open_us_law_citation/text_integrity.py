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
* **repeated span** — a block of 395-402 characters stated twice, back to back across a
  newline, 89% of the time starting mid-sentence and sometimes mid-word. This is the
  dominant cause of COV-1A's 63,224 CFR text mismatches, and measuring it here is the
  point: against the eCFR oracle it scores precision 1.0000 / recall 0.9980 on a balanced
  993-section sample, so it can be trusted on the corpora that have **no** oracle and, for
  most states, never will. Detection is :mod:`.derived.text_integrity`; this harness only
  counts what that producer finds, so the rate and the artifact can never disagree.

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

from .derived.text_integrity import (
    MIN_REPEAT_LENGTH,
    detect_repeated_spans,
)

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
    # A row can only carry a repeat if it is long enough to hold two copies plus the
    # separator, so `checkable` is the honest denominator for the repeated-span rate --
    # scoring it against every row would dilute it with rows the defect cannot reach.
    checkable_rows: int = 0
    repeated_span_rows: int = 0
    repeated_span_blocks: int = 0
    repeated_span_chars: int = 0
    truncated_examples: list[tuple[str, str]] = field(default_factory=list)
    chrome_examples: list[tuple[str, str]] = field(default_factory=list)
    repeat_examples: list[tuple[str, int, int]] = field(default_factory=list)


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


# A repeat needs two copies plus the separator, so a shorter body cannot hold one and a
# body with no newline cannot either. Both are exact preconditions of the detector, not
# heuristics, so this filter changes the cost and never the answer -- and it keeps the
# streamed batches small on the 11 GB regulations column.
_REPEAT_SCAN_SQL = """
SELECT act_id,
       CASE WHEN text IS NOT NULL
                 AND length(text) >= ?
                 AND contains(text, chr(10))
            THEN text END AS body
FROM read_parquet(?)
"""

_REPEAT_EXAMPLE_LIMIT = 8


def _scan_repeated_spans(
    con: duckdb.DuckDBPyConnection, path: Path, rows_per_batch: int
) -> tuple[int, int, int, int, list[tuple[str, int, int]]]:
    """Stream the text column through the repeated-span producer.

    Never materialises a row-group: DuckDB streams ``text`` in vectors and this pulls a
    bounded list of *eligible* bodies at a time (CLAUDE.md's OOM invariant). Examples are
    the lexicographically smallest act_ids among the hits, so the report is byte-stable
    under any scan order, thread count, or batch size.
    """
    checkable = hit_rows = blocks = chars = 0
    examples: list[tuple[str, int, int]] = []
    # ``fetchmany`` over the streaming result, not ``to_arrow_reader``: the eligibility
    # filter below is barely a filter (most bodies are long and contain a newline), so
    # nearly the whole ~11 GB text column flows through here. An Arrow reader buffers
    # whole batches per column and OOM-killed a 14 GB box at 64 rows/batch; fetchmany
    # hands back one small list of Python strings at a time, which is dropped before the
    # next arrives.
    result = con.execute(_REPEAT_SCAN_SQL, [2 * MIN_REPEAT_LENGTH + 1, path.as_posix()])
    while True:
        rows = result.fetchmany(rows_per_batch)
        if not rows:
            break
        for act_id, body in rows:
            if body is None:
                continue
            checkable += 1
            spans = detect_repeated_spans(body)
            if not spans:
                continue
            hit_rows += 1
            blocks += len(spans)
            total = sum(span.length for span in spans)
            chars += total
            if len(examples) < _REPEAT_EXAMPLE_LIMIT or act_id < examples[-1][0]:
                examples.append((act_id, len(spans), total))
                examples.sort()
                del examples[_REPEAT_EXAMPLE_LIMIT:]
        del rows
    return checkable, hit_rows, blocks, chars, examples


def scan_file(
    path: str | Path,
    *,
    memory_limit: str = "3GB",
    temp_dir: Path | None = None,
    rows_per_batch: int = 128,
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
        checkable, repeat_rows, repeat_blocks, repeat_chars, repeat_examples = (
            _scan_repeated_spans(con, path, rows_per_batch)
        )
    finally:
        con.close()
    return FileIntegrity(
        corpus_file=path.name.replace(".parquet", ""),
        rows=int(counts[0]), non_null_text=int(counts[1]),
        truncated_head=int(counts[2]), ui_chrome=int(counts[3]),
        impossible_title_cites=int(counts[4]), corrupt_xref_titles=int(xref),
        checkable_rows=checkable,
        repeated_span_rows=repeat_rows,
        repeated_span_blocks=repeat_blocks,
        repeated_span_chars=repeat_chars,
        truncated_examples=[(a, t) for a, t in trunc],
        chrome_examples=[(a, t) for a, t in chrome],
        repeat_examples=repeat_examples,
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
    A("## Repeated spans")
    A("")
    A("A block of 395-402 characters stated **twice, back to back across a newline**. "
      "`checkable` is rows long enough to hold two copies plus the separator and "
      "containing a newline — the exact precondition for the defect, so it is the "
      "denominator the rate is against; scoring it against every row would dilute it "
      "with rows the defect cannot reach.")
    A("")
    A("| file | checkable rows | rows with a repeated span | blocks | repeated characters |")
    A("|---|---:|---:|---:|---:|")
    for f in files:
        A(f"| {f.corpus_file} | {f.checkable_rows:,} | "
          f"{f.repeated_span_rows:,} ({_pct(f.repeated_span_rows, f.checkable_rows)}) | "
          f"{f.repeated_span_blocks:,} | {f.repeated_span_chars:,} |")
    A("")
    A("A file with **0 checkable rows** is not a clean file: it has no body carrying a "
      "newline at all, so the separator this detector requires is absent and its rate is "
      "**unknown**, not zero. Such a corpus can still be damaged in a form this producer "
      "cannot see. A `0.00%` against a large checkable count is the opposite — a positive "
      "result, and evidence the detector is not simply firing everywhere.")
    A("")
    A("This is the dominant cause of COV-1A's 63,224 CFR text mismatches: the row states "
      "part of its own text twice, so nothing is missing and nothing is wrong — it is "
      "said again. Against the pinned eCFR edition the detector scores precision 1.0000 "
      "and recall 0.9980 on a balanced 993-section sample with **zero false positives**, "
      "which is what licenses reading the rates above for corpora that have no official "
      "oracle at all. `repeated characters` counts the surplus copies (a block appearing "
      "N times contributes N-1), and is an observation, not a claim about how much text "
      "a repair would remove.")
    A("")
    for f in files:
        if not f.repeat_examples:
            continue
        A(f"Examples — {f.corpus_file} (smallest `act_id`s among the hits):")
        A("")
        for act_id, blocks, chars in f.repeat_examples:
            A(f"- `{act_id}` — {blocks} block(s), {chars:,} repeated characters")
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
    ap.add_argument("--rows-per-batch", type=int, default=128,
                    help="rows per streamed Arrow batch for the repeated-span scan; "
                         "lower it if bodies are very large.")
    args = ap.parse_args(argv)

    paths = sorted({Path(p) for pat in args.paths for p in globlib.glob(pat)})
    files = []
    for path in paths:
        print(f"scanning {path.name} ...", flush=True)
        files.append(scan_file(path, memory_limit=args.memory_limit,
                               temp_dir=args.temp_dir,
                               rows_per_batch=args.rows_per_batch))
    report = render_report(files, args.snapshot)
    if args.out:
        Path(args.out).write_text(report)
        print(f"wrote {args.out} ({len(files)} files)")
    else:
        print(report)


if __name__ == "__main__":
    main()
