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
| us_federal_regulations | 582,054 | 424,281 (72.89%) | 286,492 | 2,015,801 | 1,313,031 |
| us_federal_statutes | 54,853 | 17,533 (31.96%) | 12,286 | 64,978 | 1,641 |

## Agreement with the dataset's cross-references (de-duplicated edges)

`both` = the explicit edge is in both; `detector-only` = an explicit citation the
dataset did not list; `dataset-only` = a cross-reference the detector did not emit
(overwhelmingly bare/relative refs — the M4 population).

| File | Corpus | both | detector-only | dataset-only |
|---|---|---:|---:|---:|
| us_federal_regulations | USC | 56,406 | 967,120 | 6,838 |
| us_federal_regulations | CFR | 16,886 | 727,449 | 232,522 |
| us_federal_statutes | USC | 28,777 | 4,994 | 99,150 |
| us_federal_statutes | CFR | 0 | 1,081 | 0 |

## Impossible-title detections (precision tripwire)

Distinct detected edges whose title is outside its code's range — false positives by
construction, needing no labelled set. See the section below for the cause.

| File | USC out-of-range | CFR out-of-range |
|---|---:|---:|
| us_federal_regulations | 0 | 0 |
| us_federal_statutes | 0 | 0 |

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

**2. A greedy title absorbed whatever digits were adjacent.** `(?P<title>\d+)` accepts any
digit run, and at corpus scale the snapshot's text supplies many that are not titles. Tracing
the population found a single mechanism behind all of them, with the wrong digits arriving
from four different directions:

| Source of the digits | Example found in the corpus | Real citation |
|---|---|---|
| Leading digit dropped at a line break | `Implementation\n0 CFR 264.100` | 40 CFR 264.100 |
| Flattened table cell (dollar column) | `$2,453,218.\n$122,661\nU.S.C. 362(a)` | 47 U.S.C. 362(a) |
| Flattened table cell (date column) | `on January 3, 2023\nCFR 2.2` | 50 CFR 2.2 |
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
- `42 U.S.C. § 300xx`
- `42 U.S.C. § 7426`
- `42 U.S.C. § 8373`
- `42 U.S.C. § 9617`
- `43 U.S.C. § 322`
- `49 U.S.C. § 206`

