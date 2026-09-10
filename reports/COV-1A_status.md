# COV-1A — official federal provision baseline status

**Status:** CFR half complete, USC half blocked. The deterministic comparison
engine and its acceptance fixtures are implemented, and the **eCFR oracle is now
staged and checksum-pinned** — all 49 titles of the 2026-08-26 point-in-time
edition under `sha256_tree_v1`. The first real CFR scorecard is
[`COV-1A_cfr_baseline.md`](COV-1A_cfr_baseline.md).

The USC half remains unstaged (`local_path` and `sha256` still null for the USLM
edition) because `uscode.house.gov` has been unreachable; GovInfo cannot
substitute, since Open US Law's own USC is a GovInfo-HTML re-parse and the
comparison would be circular.

This status document is not itself a coverage report.

## Inventory validation (CFR)

The projection is validated against a second, independent official measurement —
the eCFR *structure* API counts pre-recorded in
[`COV-1A_ecfr_browse_counts.md`](COV-1A_ecfr_browse_counts.md), which fetch no
regulatory text at all:

- **All 49 titles match exactly on total sections: 227,521 = 227,521.**
- Reserved counts differ by 3 (6,993 here against 6,985 there), and the whole
  difference is explained. The structure API flags reserved by a **suffix** match
  on the heading, so anything after the closing bracket defeats it: 442 of 442
  headings ending at `[Reserved]` are API-flagged, and 3 of 3 carrying trailing
  text (`[Reserved].`, `[Reserved] (Rule 28).`, `[Reserved]` then a stray `]`)
  are not. All three have empty bodies, so the XML reading is the correct one.
  The remaining 5 of the 8-section gap are OFR bracket typos the projection now
  also catches (see the `empty_official_body` note below).

## Implemented first slice

[`coverage_baseline.py`](../src/open_us_law_citation/coverage_baseline.py) now
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
| present, `[Reserved]` | any | `reserved` (held out of `expected`) |
| present, empty body | any | `empty_official_body` (held out of `expected`) |
| present | 0 | `missing` |
| present | 1 | `represented` |
| present | >1, all non-null raw hashes equal | `duplicate` |
| present | >1, divergent or unavailable raw hashes | `ambiguous` |
| absent | ≥1 | `unexpected` |

The first two rows are checked **before** the candidate count, because the
official source publishes no law at those keys — so the snapshot having or
lacking a row there cannot make them represented or missing. Both are counted and
reported in their own columns, never silently dropped.

`empty_official_body` is a section the official source publishes as a heading
with no body at all, overwhelmingly an undesignated *parent*: `48 CFR 1.105` is
`<HEAD>1.105 Issuance.</HEAD>` and nothing else, because its law lives in
`1.105-1/-2/-3`, which the snapshot does carry. Scoring the parent `missing`
manufactured a **1,469-section** CFR gap — 80% of a 1,843 `missing` count whose
true size is 374 — and dragged title 48 from 98.91% to 89.56% on its own. The
flag is derived from the official bytes and is checkable rather than asserted:
whitespace collapses to the empty string under the comparison normalization, so
`empty_body` holds exactly when the stored normalized hash is the hash of `""`,
and a directly-constructed provision that claims otherwise is rejected. Null text
(text *unavailable*) stays distinct from an empty body (text available, and
officially empty).

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
is exact relative to the versioned `xml_text_nodes_newline_v2` official XML text
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
uv run open-us-law-citation coverage-baseline build-inventory \
  --corpus usc \
  --oracle-manifest oracles/v2026.08.json \
  --currency-basis "OLRC release point through Public Law 118-274, except 118-159" \
  --output data/oracles/usc-v2026.08-inventory.json
```

4. Compare the checksum-pinned dataset file and emit both artifacts.

```bash
uv run open-us-law-citation coverage-baseline compare \
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

Done on the CFR side:

- ~~stage all point-in-time eCFR titles~~ — 49 titles pinned by `sha256_tree_v1`;
- ~~validate title/section projection totals against the official browse
  inventory~~ — all 49 titles match exactly (see *Inventory validation* above);
- ~~run the real v2026.08 CFR crosswalk~~ —
  [`COV-1A_cfr_baseline.md`](COV-1A_cfr_baseline.md).

Still open:

- stage and checksum the complete OLRC USLM USC inventory, then run the USC
  crosswalk (blocked on `uscode.house.gov`);
- inspect the residual CFR unmatched sample: **374** official sections are
  genuinely missing from the snapshot, and **288 of them (77%) sit in title 7**
  — a concentration that is itself the next question, not a settled number;
- establish or retain pending CFR currency from comparison evidence (the CFR
  cutoff is still `unresolved`, so all 218,690 currency overlays read `pending`
  and the 60.81% exact-text rate is *not* evidence of staleness either way); and
- commit the byte-stable USC report.

The Markdown scorecards are committed; the full discrepancy manifests are **not**
(`reports/COV-1A_*_discrepancies.json` is gitignored). One JSON record per
official provision is ~136 MB for the CFR, and it regenerates byte-for-byte from
the checksum-pinned oracle and dataset named in the scorecard — verified by
rerunning `build-inventory` + `compare` and diffing. The scorecard is the
artifact under review; the manifest is a working file.

The discrepancy strata then become the sample frames for CFR-A1 assembly and
M0.5B1 USC anatomy, as required by [`PROPOSAL.md`](../PROPOSAL.md).
