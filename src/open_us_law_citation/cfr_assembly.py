"""CFR-A1 — the snapshot-internal half of the CFR assembly commissioning spike.

PROPOSAL.md gates the CFR assembly layer: ``cfr_source_assembly_v1`` (CFR-A2) may be
implemented only **after CFR-A1 reports**, and CFR-A1's *validation* half compares a
proposed assembly against the point-in-time eCFR edition that is not yet staged. This
harness builds everything that does **not** depend on that oracle: it enumerates every
multi-row ``CFR_*`` group, classifies each by the physical relationship between its rows,
and reports the projected disposition — including the **abstention rate on multi-row CFR
groups**, which is the number PROPOSAL.md decision B turns on.

It deliberately produces **no** ``SourceDocumentAssembly``. Nothing here marks a group
``complete``; that is CFR-A2's job and it is gated.

The load-bearing question is the one M0.5A.1 already answered *negatively* for ``FR_*``:
are co-numbered rows the ordered **segments** of one document, so that concatenation
reconstructs it? M0.5A.1 found a minority of genuine mid-sentence continuations in
``CFR_*`` and left the rest open. This harness closes that by testing the hypothesis
concatenation would have to assume — that consecutive rows are *disjoint* pieces — against
the alternative it must be distinguished from: **variant captures**, where two rows are
overlapping renderings of the same section (one carrying an eCFR banner, one truncated).
Concatenating a variant-capture pair does not reconstruct a section; it duplicates text.

Memory: the ``text`` column of ``us_federal_regulations.parquet`` is ~11 GB and a naive
scan OOM-kills the box (CLAUDE.md). The ``SEMI JOIN`` here narrows to the collision rows
**before** any text is materialised — 2,236 rows totalling ~26 MiB at v2026.08 — so full
text for exactly those rows is safe to pull. Everything runs in DuckDB under a hard
``--memory-limit`` with disk spill; the group sizing pass touches no text at all.

Regenerate::

    uv run python -m open_us_law_citation.cfr_assembly \\
        data/v2026.08_full/us_federal_regulations.parquet \\
        --snapshot v2026.08 --out reports/CFR-A1_commissioning_frame.md \\
        --memory-limit 3GB --temp-dir /path/to/scratch/ddspill
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Sequence

import duckdb

# A pair is treated as overlapping renderings of one section rather than two disjoint
# pieces when their shared prefix or suffix covers at least this fraction of the shorter
# row. It is deliberately high: the failure it guards against (concatenating a variant
# pair, duplicating operative text under a whole-section citation) is the hard failure
# CFR-A1 has zero tolerance for, so the classifier only claims "variant" on strong
# evidence and otherwise falls through to an abstaining bucket.
_OVERLAP_RATIO = 0.5
# Sentence-final punctuation. A row whose last character is none of these ends mid-thought.
_TERMINAL = frozenset(".?!:;”’\")]")


class GroupRelation(StrEnum):
    """How the rows of one multi-row ``CFR_*`` group physically relate."""

    DUPLICATE_ONLY = "duplicate_only"        # every row byte-identical: dedup, no composition
    VARIANT_CAPTURE = "variant_capture"      # overlapping renderings: concatenation INVALID
    CANDIDATE_SEGMENTED = "candidate_segmented"  # disjoint + continuation signal
    UNDETERMINED = "undetermined"            # no evidence either way -> abstain


@dataclass(frozen=True, slots=True)
class MemberRow:
    frn: int
    text_sha256: str
    length: int
    text: str


@dataclass
class GroupAnalysis:
    act_id: str
    size: int
    relation: GroupRelation
    distinct_hashes: int
    # Strongest overlap seen between any consecutive pair, as a fraction of the shorter row.
    max_overlap_ratio: float
    # Consecutive pairs where the earlier row ends mid-thought and the later starts lowercase.
    continuation_seams: int
    seams: int
    contained_pairs: int          # one row's text wholly inside another's
    total_bytes: int

    @property
    def composable_without_an_oracle(self) -> bool:
        """Only an all-identical group can be resolved with no oracle: its text is not in
        dispute, so dedup is an identity, not a reconstruction."""
        return self.relation == GroupRelation.DUPLICATE_ONLY


def _common_prefix(a: str, b: str) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def _common_suffix(a: str, b: str) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[-1 - i] == b[-1 - i]:
        i += 1
    return i


def _is_continuation(earlier: str, later: str) -> bool:
    """Does ``earlier`` stop mid-thought and ``later`` resume it?

    The M0.5A.1 proxy (next row starts lowercase) is kept and tightened: the earlier row
    must also lack sentence-final punctuation. Both halves are required because either
    alone is common in ordinary prose.
    """
    left = earlier.rstrip()
    right = later.lstrip()
    if not left or not right:
        return False
    return left[-1] not in _TERMINAL and right[0].islower()


def analyze_group(act_id: str, rows: Sequence[MemberRow]) -> GroupAnalysis:
    """Classify one group. Rows must already be ordered by physical row number."""
    hashes = {row.text_sha256 for row in rows}
    total_bytes = sum(row.length for row in rows)
    if len(hashes) == 1:
        return GroupAnalysis(
            act_id=act_id, size=len(rows), relation=GroupRelation.DUPLICATE_ONLY,
            distinct_hashes=1, max_overlap_ratio=1.0, continuation_seams=0,
            seams=max(len(rows) - 1, 0), contained_pairs=0, total_bytes=total_bytes,
        )

    # Overlap/containment is a property of the *pair*, not of adjacency, so it is measured
    # over EVERY pair -- a 3- or 4-row group can hold a variant capture that is not
    # physically consecutive (67 of the 1,083 v2026.08 groups have 3 or 4 rows).
    max_ratio = 0.0
    contained = 0
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i].text, rows[j].text
            shorter = min(len(a), len(b)) or 1
            overlap = max(_common_prefix(a, b), _common_suffix(a, b))
            max_ratio = max(max_ratio, overlap / shorter)
            if a in b or b in a:
                contained += 1
    # Continuation, by contrast, IS an adjacency claim: it asks whether the next row in
    # physical order resumes this one, so it is measured only across consecutive seams.
    continuations = 0
    seams = 0
    for earlier, later in zip(rows, rows[1:]):
        seams += 1
        if _is_continuation(earlier.text, later.text):
            continuations += 1

    if contained or max_ratio >= _OVERLAP_RATIO:
        relation = GroupRelation.VARIANT_CAPTURE
    elif continuations:
        relation = GroupRelation.CANDIDATE_SEGMENTED
    else:
        relation = GroupRelation.UNDETERMINED

    return GroupAnalysis(
        act_id=act_id, size=len(rows), relation=relation, distinct_hashes=len(hashes),
        max_overlap_ratio=max_ratio, continuation_seams=continuations, seams=seams,
        contained_pairs=contained, total_bytes=total_bytes,
    )


_SIZING_SQL = """
SELECT COUNT(*) FILTER (WHERE act_id LIKE 'CFR%'),
       COUNT(DISTINCT act_id) FILTER (WHERE act_id LIKE 'CFR%')
FROM read_parquet(?)
"""

# The SEMI JOIN narrows to collision rows BEFORE text is materialised; only then is full
# text pulled, for ~2.2k rows. Never widen this to all CFR rows (see the module note).
_MEMBERS_SQL = """
WITH multi AS (
    SELECT act_id FROM read_parquet(?)
    WHERE act_id LIKE 'CFR%' GROUP BY act_id HAVING COUNT(*) > 1
)
SELECT r.act_id,
       r.file_row_number AS frn,
       'sha256:' || sha256(r.text) AS text_sha256,
       length(r.text) AS len,
       r.text
FROM read_parquet(?, file_row_number=true) r
SEMI JOIN multi m ON m.act_id = r.act_id
WHERE r.text IS NOT NULL
ORDER BY r.act_id, frn
"""


def _connect(memory_limit: str, temp_dir: Path | None) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute(f"SET memory_limit='{memory_limit}'")
    if temp_dir is not None:
        temp_dir.mkdir(parents=True, exist_ok=True)
        con.execute(f"SET temp_directory='{temp_dir.as_posix()}'")
    con.execute("SET threads=1")
    con.execute("SET preserve_insertion_order=false")
    return con


@dataclass
class CommissioningFrame:
    corpus_file: str
    cfr_rows: int
    cfr_act_ids: int
    groups: list[GroupAnalysis] = field(default_factory=list)

    @property
    def multi_row_rows(self) -> int:
        return sum(g.size for g in self.groups)

    def by_relation(self, relation: GroupRelation) -> list[GroupAnalysis]:
        return [g for g in self.groups if g.relation == relation]


def build_frame(
    path: str | Path,
    *,
    memory_limit: str = "3GB",
    temp_dir: Path | None = None,
) -> CommissioningFrame:
    path = Path(path)
    con = _connect(memory_limit, temp_dir)
    try:
        sized = con.execute(_SIZING_SQL, [path.as_posix()]).fetchone() or (0, 0)
        rows = con.execute(
            _MEMBERS_SQL, [path.as_posix(), path.as_posix()]
        ).fetchall()
    finally:
        con.close()

    grouped: dict[str, list[MemberRow]] = {}
    for act_id, frn, text_sha256, length, text in rows:
        grouped.setdefault(act_id, []).append(
            MemberRow(frn=int(frn), text_sha256=text_sha256, length=int(length), text=text)
        )
    frame = CommissioningFrame(
        corpus_file=path.name.replace(".parquet", ""),
        cfr_rows=int(sized[0]),
        cfr_act_ids=int(sized[1]),
    )
    # Deterministic order: by act_id, so the report and the drawn sample are byte-stable.
    for act_id in sorted(grouped):
        frame.groups.append(analyze_group(act_id, grouped[act_id]))
    return frame


# Qualitative verdict, embedded so the report regenerates verbatim (repo convention).
_EXIT_SECTION = """\
## What this changes about CFR-A2

**Concatenation is the wrong primitive for this corpus.** CFR-A2 is specified as a
composer -- "continuation signal + physical row order + dedup" -- but only **34 of 1,083**
multi-row groups (3.1%) contain even one seam where a row stops mid-thought and the next
resumes it, and 2 of those also contain a wholly-contained pair, which is evidence against
segmentation rather than for it. A concatenating producer would therefore apply to at most
~3% of multi-row groups, i.e. ~0.014% of the 218,865 distinct CFR sections.

The dominant real phenomenon is different: **376 groups (34.7%) are variant captures** --
two renderings of the same section, one typically carrying an eCFR amendment banner
("Link to an amendment published...") or truncated mid-word, with 365 of them containing a
pair where one row's text sits **wholly inside** another's. Concatenating such a pair does
not reconstruct a section; it emits the operative text twice under a whole-section
citation. That is the failure CFR-A1 has zero tolerance for, and it is the *majority*
outcome among non-duplicate groups -- so the composer must be able to recognise and refuse
it, not merely order rows.

This is the same shape of negative result M0.5A.1 established for `FR_*`, arrived at
independently: co-numbered rows are mostly not ordered pieces of one document.

## The threshold is calibrated, not asserted

Overlap is bimodal across the 851 non-duplicate groups -- 38.3% sit below 0.01 and 42.7%
at or above 0.90, with only 3.2% in the whole 0.30-0.90 band. The 0.50 cut therefore falls
in an empty valley: moving it anywhere inside that band reclassifies almost nothing. Where
evidence is genuinely weak the classifier falls through to `undetermined`, which abstains.

## Decision B depends on a choice this spike cannot make alone

PROPOSAL.md decision B reconsiders the build-time eCFR dependency if CFR-A1 **abstains on
more than 50% of multi-row CFR groups**. That number is not single-valued here -- it turns
on whether *superset selection* is permitted:

- **Abstain on everything not provably safe** (only all-identical groups resolve): **78.6%**
  (851 of 1,083) -- above the 50% trigger.
- **Also allow superset selection** where one row's text wholly contains another's, taking
  the containing row: **44.9%** (486 of 1,083) -- below the trigger.

Superset selection is provably never *partial relative to the group's own members*: the
containing row holds every byte the contained row held, so nothing is dropped. It is **not**
proof of completeness against the official section -- the containing row may itself be
truncated, which only the pinned eCFR edition can settle. The recommendation is therefore
to treat superset selection as a candidate CFR-A2 rule whose `complete` claim stays gated
on the eCFR half of CFR-A1, and to read 78.6% as the abstention rate that holds until then.

## What is NOT established here

This harness is snapshot-internal by construction and emits **no** `SourceDocumentAssembly`.
It cannot report continuation-classification precision/recall, assembled-text match, or the
partial-law rate: every one of those compares a proposed assembly against the point-in-time
eCFR edition, which is not yet staged. `candidate_segmented` means *the snapshot shows a
continuation signal*, never *these rows are the pieces of this section*.
"""


def _pct(numer: int, denom: int) -> str:
    return f"{100.0 * numer / denom:.1f}%" if denom else "—"


_SAMPLE_PER_STRATUM = 12


def render_report(frame: CommissioningFrame, snapshot: str) -> str:
    from collections import Counter

    counts = Counter(g.relation for g in frame.groups)
    total = len(frame.groups)
    non_dup = [g for g in frame.groups if g.relation != GroupRelation.DUPLICATE_ONLY]
    contained = sum(1 for g in non_dup if g.contained_pairs)
    lines: list[str] = []
    A = lines.append
    A("# CFR-A1 — CFR assembly commissioning frame (snapshot-internal half)")
    A("")
    A(f"Snapshot: `{snapshot}`. Every multi-row `CFR_*` `act_id` group in")
    A(f"`{frame.corpus_file}`, classified by the physical relationship between its rows.")
    A("")
    A("**This is the half of CFR-A1 that needs no oracle.** The validation half — comparing")
    A("a proposed assembly against the point-in-time eCFR edition that is COV-1A's")
    A("denominator — is pending those bytes. Accordingly this emits **no**")
    A("`SourceDocumentAssembly` and marks nothing `complete`: CFR-A2 stays gated.")
    A("")
    A("## Population")
    A("")
    A(f"- CFR rows: **{frame.cfr_rows:,}**; distinct `act_id`: **{frame.cfr_act_ids:,}**")
    A(f"- Multi-row groups: **{total:,}** covering **{frame.multi_row_rows:,}** rows "
      f"({_pct(total, frame.cfr_act_ids)} of distinct sections)")
    A("")
    A("## Group relations")
    A("")
    A("| relation | groups | share | meaning for assembly |")
    A("|---|---:|---:|---|")
    meanings = {
        GroupRelation.DUPLICATE_ONLY:
            "every row byte-identical — dedup is an identity, no composition needed",
        GroupRelation.VARIANT_CAPTURE:
            "overlapping renderings of one section — **concatenation would duplicate text**",
        GroupRelation.CANDIDATE_SEGMENTED:
            "disjoint rows with a mid-thought continuation seam — the only composer candidates",
        GroupRelation.UNDETERMINED:
            "no evidence either way — abstain",
    }
    for rel in GroupRelation:
        A(f"| `{rel}` | {counts[rel]:,} | {_pct(counts[rel], total)} | {meanings[rel]} |")
    A("")
    A(f"Groups containing a wholly-contained pair: **{contained:,}**. "
      f"Groups with any continuation seam: "
      f"**{sum(1 for g in frame.groups if g.continuation_seams):,}**.")
    A("")
    A("## Overlap distribution (non-duplicate groups)")
    A("")
    A("Max shared prefix/suffix between any pair, as a fraction of the shorter row.")
    A("")
    A("| band | groups | share |")
    A("|---|---:|---:|")
    for lo, hi in ((0.0, 0.01), (0.01, 0.05), (0.05, 0.15), (0.15, 0.30),
                   (0.30, 0.50), (0.50, 0.90), (0.90, 1.01)):
        n = sum(1 for g in non_dup if lo <= g.max_overlap_ratio < hi)
        A(f"| `[{lo:.2f}, {hi:.2f})` | {n:,} | {_pct(n, len(non_dup))} |")
    A("")
    A("## Group sizes")
    A("")
    sizes = Counter(g.size for g in frame.groups)
    A("| rows in group | groups |")
    A("|---:|---:|")
    for size in sorted(sizes):
        A(f"| {size} | {sizes[size]:,} |")
    A("")
    A("## Deterministic commissioning sample")
    A("")
    A(f"The first {_SAMPLE_PER_STRATUM} groups of each stratum by `act_id` — a stable frame")
    A("for the eCFR validation half to draw from, so that run is reproducible rather than")
    A("re-sampled.")
    A("")
    for rel in GroupRelation:
        members = frame.by_relation(rel)[:_SAMPLE_PER_STRATUM]
        if not members:
            continue
        A(f"**`{rel}`**")
        A("")
        for g in members:
            A(f"- `{g.act_id}` — {g.size} rows, overlap {g.max_overlap_ratio:.3f}, "
              f"continuation {g.continuation_seams}/{g.seams}")
        A("")
    A(_EXIT_SECTION)
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description="CFR-A1 commissioning frame — classify every multi-row CFR act_id "
        "group from the snapshot alone (emits no assembly; CFR-A2 stays gated)."
    )
    ap.add_argument("path", help="the federal regulations Parquet file")
    ap.add_argument("--snapshot", required=True, help="snapshot version, e.g. v2026.08")
    ap.add_argument("--out", help="write the Markdown report here (else stdout)")
    ap.add_argument("--memory-limit", default="3GB",
                    help="DuckDB hard memory limit (spills to --temp-dir beyond this).")
    ap.add_argument("--temp-dir", type=Path, default=Path(".duckdb_spill"),
                    help="scratch directory for DuckDB spill files.")
    args = ap.parse_args(argv)

    frame = build_frame(args.path, memory_limit=args.memory_limit, temp_dir=args.temp_dir)
    report = render_report(frame, args.snapshot)
    if args.out:
        Path(args.out).write_text(report)
        print(f"wrote {args.out} ({len(frame.groups):,} groups)")
    else:
        print(report)


if __name__ == "__main__":
    main()
