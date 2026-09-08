# M2 citation-parser self-check

Snapshot: `v2026.08`. Parser methods: `usc_grammar_v1`, `cfr_grammar_v2`.

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
| us_federal_regulations | 220,018 | 219,971 | 218,268 | 1,703 | 0 | 47 | 99.98% |
| **all** | **220,018** | **219,971** | **218,268** | **1,703** | **0** | **47** | **99.98%** |

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

## Citation format (what the grammar targets)

Each row stores `citation` (with edition year) and `citation_short` (without). For USC and
codified CFR the shape is exact and uniform across the whole corpus:

```
citation        =  citation_short + " (" + year + ")"
citation_short  =  <title> <CODE> § <section>
```

| Corpus | Rows | Template | Example (`citation`) | Conformance |
|---|---:|---|---|---:|
| USC | 54,853 | `<title> U.S.C. § <section> (<year>)` | `42 U.S.C. § 1983 (2024)` | 100.00% |
| CFR (codified) | 220,018 | `<title> C.F.R. § <section> (<year>)` | `5 C.F.R. § 330.601 (2026)` | 100.00% |
| Federal Register (`FR_*`) | 362,036 | `<volume> FR <page>` | `71 FR 8523` | different format |

- `citation_short` matches `^<n> U.S.C. § ` for 100% of USC rows and `^<n> C.F.R. § ` for
  100% of codified CFR rows; `citation == citation_short || ' (' || year || ')'` holds for
  100% of both (and for none of the FR rows).
- The USC edition `<year>` is uniformly `2024` (the GovInfo USCODE-2024 edition); CFR carries
  its source year.
- Federal Register is a `volume FR page` locator (`71 FR 8523`) — no `§`, no title/section —
  so all 362,036 `FR_*` rows are excluded from the parser (promulgation records, not codified
  sections) and form the expected-abstention baseline above.

### The `<section>` sub-grammar (the one component with real structure)

| Corpus | Shape | Examples |
|---|---|---|
| USC | digits + optional letters + optional `_digits` | `1983`, `1613a`, `77aa`, `1749aaa`, `222e_2` |
| CFR | `part.rest`; part may carry a letter (`261a`) or hyphens (`101-6`); rest carries digits/letters/hyphens and **embedded** `(...)` / `(T)` | `330.601`, `240.10b-5`, `1864.0-3`, `41.6151(a)-1`, `240.11a1-4(T)` |

The load-bearing USC-vs-CFR asymmetry (why the CFR producer is `cfr_grammar_v2`): in USC a
subsection like `(a)` is a *separate* pointer and never appears in `section_number`; in CFR
the parenthesised/`(T)` material is *part of the section identity* and lives inside
`section_number`, so v2 keeps it in `parsed_section`.

Beyond the `§` forms, the grammar also accepts the variants people write — `42 USC 1983`,
`42 U.S.C.A. § 1983`, `Section 1983 of Title 42` — but the two fields above are the dataset's
own canonical shape, which is what makes them a clean full-corpus labelled set. The only
citation strings that do not fit are the abstentions listed above (14 CFR Part 241's dotless
numbering and a handful of source typos).

