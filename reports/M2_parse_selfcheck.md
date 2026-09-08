# M2 citation-parser self-check

Snapshot: `v2026.08`. Parser methods: `usc_grammar_v1`, `cfr_grammar_v1`.

Each USC/CFR row's own `citation_short` (or `citation`) is parsed and its
`(title, section)` compared to the row's structured `title_number` /
`section_number` — the Stage-B parse metric on the dataset's own labels, with no
external oracle. `exact` = parsed and both structured fields present and agree;
`recovered` = parsed where a structured field was **null** and nothing present
disagreed (the parser backfills the unreliable flat columns — an M0 finding);
`mismatch` = a *present* structured field disagrees (a real grammar gap, never
coerced); `abstained` = no confident parse. Non-USC/CFR namespaces are an
expected-abstention baseline, not scored.

## USC

| File | Rows | Parsed | Exact | Recovered | Mismatch | Abstained | Correct rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| us_federal_statutes | 54,853 | 54,853 | 54,853 | 0 | 0 | 0 | 100.00% |
| **all** | **54,853** | **54,853** | **54,853** | **0** | **0** | **0** | **100.00%** |

## CFR

| File | Rows | Parsed | Exact | Recovered | Mismatch | Abstained | Correct rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| us_federal_regulations | 220,018 | 218,513 | 216,807 | 1,701 | 5 | 1,505 | 99.31% |
| **all** | **220,018** | **218,513** | **216,807** | **1,701** | **5** | **1,505** | **99.31%** |

Mismatch examples (CFR, first 15 by citation):

| Citation | Parsed | Expected |
|---|---|---|
| `17 C.F.R. § 240.11a1-1(T)` | `T17 S'240.11a1-1'` | `T17 S'240.11a1-1(T)'` |
| `17 C.F.R. § 240.11a1-3(T)` | `T17 S'240.11a1-3'` | `T17 S'240.11a1-3(T)'` |
| `17 C.F.R. § 240.11a1-4(T)` | `T17 S'240.11a1-4'` | `T17 S'240.11a1-4(T)'` |
| `17 C.F.R. § 240.11a2-2(T)` | `T17 S'240.11a2-2'` | `T17 S'240.11a2-2(T)'` |
| `48 C.F.R. § 312.202(d)` | `T48 S'312.202'` | `T48 S'312.202(d)'` |

Abstention examples (CFR, first 15 by citation):

- `12 C.F.R. § 1222. 27`
- `14 C.F.R. § 03`
- `14 C.F.R. § 04`
- `14 C.F.R. § 1-1`
- `14 C.F.R. § 1-2`
- `14 C.F.R. § 1-3`
- `14 C.F.R. § 1-4`
- `14 C.F.R. § 1-5`
- `14 C.F.R. § 1-6`
- `14 C.F.R. § 1-7`
- `14 C.F.R. § 1-8`
- `14 C.F.R. § 10`
- `14 C.F.R. § 11`
- `14 C.F.R. § 12`
- `14 C.F.R. § 14`

## Expected-abstention baseline (non-USC/CFR namespaces)

| File | Rows | Abstained | Over-matched |
|---|---:|---:|---:|
| us_federal_regulations | 362,036 | 362,036 | 0 |

