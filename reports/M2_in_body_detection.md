# M2 corpus-scale in-body citation detection

Snapshot: `v2026.08`. The Stage-A exact-citation detector (`detect_mentions`) run
over **every row body** in each file. The scan streams through DuckDB under a hard
memory limit with disk spill, so the 11 GB regulations `text` column is never
materialised a row-group at a time (which SIGKILLs a 14 GB box). The coarse code-token
pre-filter is pushed into SQL: only bodies carrying an explicit code token are returned
to Python at all; the rest cannot contain an explicit citation.

**This is the M2/M4 boundary, not a recall gate.** M2 detects *explicit* citations; the
dataset's `cross_references_*` are dominated by **bare, same-title** in-body references
(`§ 4.1045`) that are LOCAL/RELATIVE resolution (hierarchy / M4) and that the explicit
detector correctly does not fire on — so `dataset-only` is expected, especially for CFR,
and is never a detector miss. Field presence is a comparison signal, not a recall floor.

## Detection volume

| File | Rows | Candidate bodies | With detection | USC mentions | CFR mentions |
|---|---:|---:|---:|---:|---:|
| us_federal_regulations | 582,054 | 424,281 (72.89%) | 286,497 | 2,016,146 | 1,313,439 |
| us_federal_statutes | 54,853 | 17,533 (31.96%) | 12,286 | 64,983 | 1,641 |

## Agreement with the dataset's cross-references (de-duplicated edges)

`both` = the explicit edge is in both; `detector-only` = an explicit citation the
dataset did not list; `dataset-only` = a cross-reference the detector did not emit
(overwhelmingly bare/relative refs — the M4 population).

| File | Corpus | both | detector-only | dataset-only |
|---|---|---:|---:|---:|
| us_federal_regulations | USC | 56,406 | 967,399 | 6,838 |
| us_federal_regulations | CFR | 16,886 | 727,822 | 232,522 |
| us_federal_statutes | USC | 28,778 | 4,997 | 99,149 |
| us_federal_statutes | CFR | 0 | 1,081 | 0 |

## Impossible-title detections (precision tripwire)

Distinct detected edges whose title is outside its code's range — false positives by
construction, needing no labelled set. See the section below for the cause.

| File | USC out-of-range | CFR out-of-range |
|---|---:|---:|
| us_federal_regulations | 280 | 373 |
| us_federal_statutes | 4 | 0 |

Examples:

- `0 C.F.R. § 17.11(h))`
- `0 C.F.R. § 194.67`
- `0 C.F.R. § 52.1870`
- `0 C.F.R. § 740.4(c)(4)`
- `0 C.F.R. § 773.14(c)`
- `0 C.F.R. § 98.84(d)`
- `100 C.F.R. § 100.101`
- `531 C.F.R. § 4.168(a)`
- `2023 C.F.R. § 2.2`
- `147 U.S.C. § 19`

## Precision limits found at corpus scale

The Stage-A gold set (36 hand-labelled passages) measures precision 1.000, but it is small
by construction. Running the same detector over every federal body surfaced two defect
classes it did not cover. Both are reported here rather than quietly absorbed.

**1. List members folded their subsection into the section — fixed.** `47 U.S.C. §§ 154(i),
4(i)` emitted the continuation items as section `4(i)` while the *primary* form of the same
citation splits to section `4` + subsection `(i)`, so one provision produced two different
edges. `_USC_LIST_SPLIT` now splits list members exactly like primaries (CFR is deliberately
not split — there parenthesised material is part of the section identity). Regression-tested;
the numbers above are post-fix.

**2. A greedy title can absorb a preceding number — open.** `Pub. L. 95-147 U.S.C. 19`
parses as title **147**, because `(?P<title>\d+)` takes every adjacent digit. The counts
below are the measurement, not an estimate: a title outside its code's range (USC 1-54,
CFR 1-50) cannot name real law, so every one is a false positive with no labelling needed.
This is left open deliberately — constraining the title to a valid range is a grammar-policy
change to `citation_parser`, outside the scope of this scan.

A third, smaller observation is **not** a detector defect: two `us_federal_statutes` bodies
contain `\n0 U.S.C. 6311` / `\n0 U.S.C. 4501`, where the snapshot's own text lost the
line-leading `(2` / `[5`. The detector faithfully reports the bytes it was given; repairing
them would mean guessing the missing digit, which the project's abstain-rather-than-guess
rule forbids.

## Detector-only USC edges (sample) — explicit cross-title cites in bodies

- `5 U.S.C. § 5901`
- `7 U.S.C. § 1622b`
- `7 U.S.C. § 2034`
- `7 U.S.C. § 608`
- `7 U.S.C. § 6521`
- `8 U.S.C. § 1351`
- `10 U.S.C. § 3321`
- `16 U.S.C. § 1506`
- `16 U.S.C. § 906`
- `21 U.S.C. § 826`
- `25 U.S.C. § 3601`
- `28 U.S.C. § 2106`
- `33 U.S.C. § 571`
- `38 U.S.C. § 5712`
- `42 U.S.C. § 7426`
- `42 U.S.C. § 8373`
- `42 U.S.C. § 9617`
- `43 U.S.C. § 322`
- `49 U.S.C. § 206`
- `147 U.S.C. § 19`

