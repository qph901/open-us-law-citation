# M2 corpus-scale in-body citation detection

Snapshot: `v2026.08`. The Stage-A exact-citation detector (`detect_mentions`) run
over **every row body** in each file, row-group-bounded (never materialising the 11 GB
regulations `text` column). A vectorised Arrow pre-filter Python-scans only bodies that
carry an explicit code token; the rest cannot contain an explicit citation.

**This is the M2/M4 boundary, not a recall gate.** M2 detects *explicit* citations; the
dataset's `cross_references_*` are dominated by **bare, same-title** in-body references
(`§ 4.1045`) that are LOCAL/RELATIVE resolution (hierarchy / M4) and that the explicit
detector correctly does not fire on — so `dataset-only` is expected, especially for CFR,
and is never a detector miss. Field presence is a comparison signal, not a recall floor.

## Detection volume

| File | Rows | Candidate bodies | With detection | USC mentions | CFR mentions |
|---|---:|---:|---:|---:|---:|
| us_federal_statutes | 54,853 | 17,533 (31.96%) | 12,286 | 64,983 | 1,641 |

## Agreement with the dataset's cross-references (de-duplicated edges)

`both` = the explicit edge is in both; `detector-only` = an explicit citation the
dataset did not list; `dataset-only` = a cross-reference the detector did not emit
(overwhelmingly bare/relative refs — the M4 population).

| File | Corpus | both | detector-only | dataset-only |
|---|---|---:|---:|---:|
| us_federal_statutes | USC | 28,778 | 4,997 | 99,149 |
| us_federal_statutes | CFR | 0 | 1,081 | 0 |

## Detector-only USC edges (sample) — explicit cross-title cites in bodies

- `10 U.S.C. § 101`
- `10 U.S.C. § 10147`
- `10 U.S.C. § 10148`
- `10 U.S.C. § 10154`
- `10 U.S.C. § 10216`
- `10 U.S.C. § 10217`
- `10 U.S.C. § 10218`
- `10 U.S.C. § 10505`
- `10 U.S.C. § 10506`
- `10 U.S.C. § 10541`
- `10 U.S.C. § 10543`
- `10 U.S.C. § 1142`
- `10 U.S.C. § 2004`
- `10 U.S.C. § 2005`
- `10 U.S.C. § 2007`
- `10 U.S.C. § 2012`
- `10 U.S.C. § 2013`
- `10 U.S.C. § 2016`
- `10 U.S.C. § 2017`
- `10 U.S.C. § 2031`

