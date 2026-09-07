# COV-1A — official federal provision baseline status

**Status:** in progress. The deterministic comparison engine and its acceptance
fixtures are implemented. No real coverage percentage is reported yet because the
official USC and eCFR bytes in [`oracles/v2026.08.json`](../oracles/v2026.08.json)
are intentionally still unstaged (`local_path` and `sha256` are null).

This status document is not a coverage report. The first USC/CFR scorecards will
be generated only after the complete official provision inventories have been
staged and checksum-pinned.

## Implemented first slice

[`coverage_baseline.py`](../src/open_us_law_coverage/coverage_baseline.py) now
provides:

- a canonical federal provision key: `(US, corpus, title, section)`;
- checksum-verified projection of USLM `<section>` and eCFR `TYPE="SECTION"`
  elements into hash-only official provision inventories;
- title-level official currency records, including explicit overrides where an
  edition is not uniform;
- streaming extraction of compact Open US Law provision fingerprints (the full
  11 GB CFR text column is never retained in memory);
- deterministic official-to-dataset crosswalks and classifications;
- byte-stable JSON discrepancy manifests and Markdown scorecards; and
- a CLI that refuses to compare an inventory whose oracle provenance differs
  from the staged registry.

The hermetic acceptance suite is in
[`test_coverage_baseline.py`](../tests/test_coverage_baseline.py). It covers
zero/one/multiple candidates, identical duplicates, divergent ambiguities,
dataset-only keys, stale and unresolved cutoffs, USC-anatomy and CFR-assembly
pending states, hyphenated CFR sections, checksum failure, official XML
projection, title-level currency, and output stability under shuffled inputs.
Both count tables and fixed four-decimal percentages use the official provision
count as their denominator; the preliminary represented percentage is explicitly
labeled structural rather than final accurate-law coverage.

## Metric contract

The official inventory is always the denominator. For each official key:

| Official key | Dataset candidates | Structural result |
|---|---:|---|
| present | 0 | `missing` |
| present | 1 | `represented` |
| present | >1, all non-null raw hashes equal | `duplicate` |
| present | >1, divergent or unavailable raw hashes | `ambiguous` |
| absent | ≥1 | `unexpected` |

`represented` is deliberately narrow: exactly one Open US Law candidate for the
official key. Currency and text are separate dimensions, so a structurally
represented provision can still be `stale`, text-mismatched, or text-pending.
`stale` is emitted only when both cutoffs are established and the dataset cutoff
precedes the official title cutoff. An unresolved CFR content cutoff remains
`pending`; a row's `year` is not silently promoted into a legal-content date.

Text results are `exact`, `normalized_only`, `mismatch`,
`pending_usc_anatomy`, `pending_cfr_assembly`, or `unavailable`. Normalization is
Unicode NFC plus whitespace collapse only; punctuation and case are preserved.
The reported normalized-agreement count includes exact matches. The exact metric
is exact relative to the versioned `xml_text_nodes_newline_v1` official XML text
projection. A USC raw mismatch remains pending until anatomy can separate
operative text from editorial material. A multi-row CFR key remains pending until
assembly establishes whether and how its rows compose.

Federal Register (`FR_*`) rows are counted as excluded promulgation-record
inventory and are never included in the codified-CFR denominator.

## Reproduction path

1. Stage the complete official source bytes at the release/date already named in
   the oracle registry. A single official XML/ZIP is hashed byte-for-byte. A
   directory of unmodified per-title eCFR XML responses uses
   `sha256_tree_v1`, which hashes each sorted relative path and raw file hash.
2. Set `local_path` and `sha256` in the registry only after the complete source
   hash has been verified.
3. Build the normalized inventory. The command records an explicit currency basis
   for every observed title; `--title-cutoffs` accepts a JSON object of title/date
   overrides.

```bash
uv run open-us-law-coverage coverage-baseline build-inventory \
  --corpus usc \
  --oracle-manifest oracles/v2026.08.json \
  --currency-basis "OLRC release point through Public Law 118-274, except 118-159" \
  --output data/oracles/usc-v2026.08-inventory.json
```

4. Compare the checksum-pinned dataset file and emit both artifacts.

```bash
uv run open-us-law-coverage coverage-baseline compare \
  --official-inventory data/oracles/usc-v2026.08-inventory.json \
  --oracle-manifest oracles/v2026.08.json \
  --dataset data/v2026.08_full/us_federal_statutes.parquet \
  --dataset-sha256 2ac5d69e23ba11a9592a06ce5e4c964d69ce8275d3635e5b3476c72860ff66c6 \
  --snapshot v2026.08 \
  --json-output reports/COV-1A_usc_discrepancies.json \
  --markdown-output reports/COV-1A_usc_baseline.md
```

Repeat for CFR using the point-in-time eCFR directory. The CFR report will retain
currency as pending until comparison evidence establishes the dataset's actual
legal-content cutoff; it will not substitute the repository commit date.

## Remaining COV-1A work

- stage and checksum the complete OLRC USLM/GovInfo-aligned USC inventory;
- stage all point-in-time eCFR titles for the explicit historical comparison date;
- validate title/section projection totals against each official browse inventory
  (the CFR side is pre-measured in
  [`COV-1A_ecfr_browse_counts.md`](COV-1A_ecfr_browse_counts.md): 220,536 active /
  227,521 total official sections as of 2026-08-26 — the snapshot's 220,018 CFR rows
  track the **active** count, so `_ecfr_provisions` must treat `reserved` sections as
  their own stratum, not `missing`);
- run both real v2026.08 crosswalks and inspect deterministic unmatched samples;
- establish or retain pending CFR currency from comparison evidence; and
- commit the byte-stable USC/CFR reports and discrepancy manifests.

The discrepancy strata then become the sample frames for CFR-A1 assembly and
M0.5B1 USC anatomy, as required by [`PROPOSAL.md`](../PROPOSAL.md).
