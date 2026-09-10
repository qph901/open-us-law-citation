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
- Reserved counts differ by **16** (7,001 here against 6,985 there), and every
  one of the 16 is accounted for. All are empty-bodied sections the XML marks as
  reserved, so the projection is the stricter and more correct reading in each
  case:
  - **3** — the structure API flags reserved by a **suffix** match on the
    heading, so anything after the closing bracket defeats it. 442 of 442
    headings ending at `[Reserved]` are API-flagged; 3 of 3 carrying trailing
    text (`[Reserved].`, `[Reserved] (Rule 28).`, `[Reserved]` then a stray `]`)
    are not.
  - **5** — OFR bracket typos (`[Reserved`, `Reserved]`, `]Reserved]`,
    `{Reserved]`) that a strict `\[reserved\]` missed; see `_ECFR_RESERVED_RE`.
  - **8** — the marker landed in the section **body** rather than its `<HEAD>`;
    see *One defect this investigation found and fixed* below.

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
manufactured a **1,469-section** CFR gap — 80% of a 1,843 `missing` count that is
in truth 366 — and dragged title 48 from 98.91% to 89.56% on its own. The
flag is derived from the official bytes and is checkable rather than asserted:
whitespace collapses to the empty string under the comparison normalization, so
`empty_body` holds exactly when the stored normalized hash is the hash of `""`,
and a directly-constructed provision that claims otherwise is rejected. Null text
(text *unavailable*) stays distinct from an empty body (text available, and
officially empty).

`represented` is deliberately narrow: exactly one Open US Law candidate for the
official key. Currency and text are separate dimensions, so a structurally
represented provision can still be `stale`, text-mismatched, or text-pending.
`stale` is emitted only from **per-provision** evidence: the provision's own last
official amendment date (`official_amendment_date`) falls after the snapshot
cutoff. A corpus-level date gap alone is not staleness and abstains to `pending`
— see *Why currency still reads `pending` for every provision* below. An
unresolved content cutoff is likewise `pending`; a row's `year` is never silently
promoted into a legal-content date.

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
- ~~inspect the residual CFR unmatched sample~~ — see *What the 366 missing
  sections are* below; **every one is accounted for, none unexplained**;
- ~~establish or retain pending CFR currency from comparison evidence~~ — the CFR
  cutoff is **established at 2026-08-12**; see *The CFR content cutoff,
  established* below;
- stage the eCFR versioner as a pinned oracle input so `stale` can be decided per
  provision rather than abstaining; and
- commit the byte-stable USC report.

The Markdown scorecards are committed; the full discrepancy manifests are **not**
(`reports/COV-1A_*_discrepancies.json` is gitignored). One JSON record per
official provision is ~136 MB for the CFR, and it regenerates byte-for-byte from
the checksum-pinned oracle and dataset named in the scorecard — verified by
rerunning `build-inventory` + `compare` and diffing. The scorecard is the
artifact under review; the manifest is a working file.

The discrepancy strata then become the sample frames for CFR-A1 assembly and
M0.5B1 USC anatomy, as required by [`PROPOSAL.md`](../PROPOSAL.md).

## What the 366 missing sections are

The residual `missing` count is small enough to characterize completely, so it
was — by reading what the *official* source publishes at each key. Every one is
accounted for:

| what eCFR publishes there | sections |
|---|---:|
| a bare cross-reference stub (`See § 1000.3.`) | 291 |
| a section in a part the snapshot carries under an older numbering | 36 |
| a terse plain-language answer (`No.`, `60 days.`) | 15 |
| substantive text that postdates the snapshot | 15 |
| an eCFR amendment banner and nothing else | 9 |

### Cross-reference stubs (291)

**The dominant class is one shape in one place.** 284 of the 291 are in title 7
parts 1000-1199, the federal milk marketing orders. Those orders are
parallel-structured: each restates the same section skeleton, and where a section
does not vary by order it incorporates the general provisions of part 1000 by
reference rather than repeating them — `§ 1001.3 Route disposition.` has the
complete body `See § 1000.3.`

Within parts 1000-1199 the separation is total:

- 720 official sections; **284 missing, and every one of them is a stub**;
- **zero** missing sections there are anything but a stub;
- all 284 stubs in those parts are missing — 100%, not a tendency;
- part **1000 itself, the target of every reference, is fully present** (34
  represented, 4 reserved, 0 missing).

The stubs are absent from the snapshot outright, not mis-keyed: a direct lookup
for `1001.3`, `1001.5`, `1001.40`, `1001.86` returns no row, while `1000.3` and
`1000.5` are both there. Median official body length is **14 characters** for the
missing stubs against **732** for title 7's 15,881 represented sections, and
**0** of those 15,881 begin with `See §`.

**These are correctly counted as `missing`, and are deliberately not carved into
a stratum.** That is the difference between this and `reserved` /
`empty_official_body`: an incorporation by reference *is* operative law.
`7 CFR 1001.3` is a real, citable provision that says the part 1000 definition
governs Order 1, so a citation to it must resolve to something, and in this
snapshot it cannot. The substantive text does sit at the referenced target, which
bounds how much law is unreachable — but it does not make the key present, and a
stratum here would be a carve-out for a gap that is genuinely a gap.

### Older numbering (36)

Two parts have been rewritten and renumbered upstream, and the snapshot carries
the previous layout. These are the first CFR **currency** evidence this project
has, and they are the reason the residual is not simply "ETL loss":

| part | official sections | dataset sections | overlap | official-only | dataset-only |
|---|---:|---:|---:|---:|---:|
| 14 CFR 1216 (NASA NEPA procedures) | 30 | 16 | 3 | 27 | 13 |
| 50 CFR 20 (migratory bird hunting) | 59 | 61 | 50 | 9 | 11 |

In part 1216 the snapshot holds `1216.102`, `1216.103` and `1216.301-.311`, none
of which exist at the pinned edition, while the edition's `1216.200-.202`,
`.400-.610`, `.700-.701`, `.800`, `.900` and `.1000` are absent from the
snapshot. Only `1216.100`, `1216.101` and `1216.300` survive in both. In part 20
the snapshot holds `20.101-20.106` and `20.151-20.155` against the edition's
`20.115-20.130`. These sections account for **all 13 and 11 of those titles'
`unexpected` (dataset-only) keys**, so the two directions corroborate: this is
one renumbering seen from both sides, not two unrelated gaps.

### Terse answers (15) and banners (9)

Fifteen sections are plain-language regulations whose entire operative body is a
short answer to a question posed in the heading — `§ 900.9 May the Secretary
require...` / `No.`; `§ 1000.521 After the receipt of the recipient's performance
report, how long...` / `60 days.`; `§ 78.42 Quarantined areas.` / `None.` These
are operative law and stay `missing`. Together with the stubs they suggest the
upstream ETL drops very short bodies, though that is a hypothesis the snapshot
alone cannot confirm.

The 9 banner-only sections are the eCFR amendment-banner phenomenon CFR-A1
already identified inside multi-row groups, appearing here as a whole section
body; two of them (`7 CFR 984.348`, `984.349`) carry the literal heading
`§ 984.348 xxx` in the official XML.

### Postdating the snapshot (15)

These carry real regulatory text and are genuinely absent, and every one of the
15 entered the CFR **between 2026-08-01 and 2026-08-24** — the four weeks before
the pinned edition. Each date is confirmed against the eCFR versioner
(`/api/versioner/v1/versions/title-{n}.json`, which returns a per-section
amendment history):

| date | section | |
|---|---|---|
| 2026-08-01 | `50 CFR 217.90` | restored (removed 2025-02-28) |
| 2026-08-14 | `33 CFR 165.T07-1030` | new; removed again 2026-09-04 |
| 2026-08-17 | `2 CFR 910.200`-`910.270` (7) | new — DOE conflict-of-interest rules |
| 2026-08-17 | `40 CFR 180.1423` | new |
| 2026-08-19 | `21 CFR 573.302` | new |
| 2026-08-20 | `50 CFR 17.90` | restored (removed 2022-08-22) |
| 2026-08-21 | `26 CFR 1.987-1T` | new |
| 2026-08-24 | `28 CFR 0.70`, `0.71` (2) | restored (removed 2025-12-10) |

Eleven are newly created sections with a single version record. The other four
looked at first like a contradiction — `28 CFR 0.70` dates to 2016 and
`50 CFR 217.90` to 2020, so why would the snapshot lack them? Because each was
**removed and later restored**, and the snapshot was taken inside the gap:

- `28 CFR 0.70` / `0.71` — added 2016-12-19, **removed 2025-12-10**, restored 2026-08-24;
- `50 CFR 17.90` — added 2021-01-19, **removed 2022-08-22**, restored 2026-08-20;
- `50 CFR 217.90` — added 2020-03-01, **removed 2025-02-28**, restored 2026-08-01.

So the snapshot is not wrong about any of them. **No missing CFR section is
unexplained.**

### The CFR content cutoff, established

The registry previously recorded the CFR `cutoff_status` as `unresolved`. It is now
**`established` at 2026-08-12**, with `residual_skew_days = 14` to the 2026-08-26
oracle edition. Two independent estimators agree, and a third check is consistent.

**Estimator 1 — removals (pure presence, no text normalization involved).** A
section removed from the CFR is either still in the snapshot or not, and nothing
about text formatting can confuse the answer:

| removed on | titles | sections | still in snapshot |
|---|---|---:|---|
| 2026-08-03 … 2026-08-12 | 10, 20, 22, 33, 43, 45, 50 | 70 | **none** — snapshot reflects every one |
| 2026-08-17 … 2026-08-25 | 14, 15, 45, 47, 50 | 79 | **all but one** — snapshot reflects none |

Title 45 appears on both sides on its own: its 2026-08-10 removals are reflected,
its 2026-08-17 removals are not. So the cutoff lies in **[2026-08-12, 2026-08-17)**.

**Estimator 2 — text agreement over represented sections.** Grouping the 15,319
represented sections that were amended since 2025 by amendment date, agreement
with the official text collapses across the same boundary while the pre-cutoff
side stays flat:

| amendments after date D | sections | agree | | amendments on/before D | agree |
|---|---:|---:|---|---|---:|
| after 2026-07-30 | 581 | 30.6% | | 2026-06-01 … D | 35.3% |
| after 2026-07-31 | 398 | 15.8% | | | 38.7% |
| after 2026-08-03 | 306 | 6.9% | | | 39.1% |
| after 2026-08-10 | 217 | 1.4% | | | 38.1% |
| after 2026-08-12 | 203 | **0.5%** | | | 37.9% |
| after 2026-08-21 | 57 | **0.0%** | | | 34.9% |

The flat 34-39% pre-cutoff column is what makes this readable: the corpus's ~30%
text-mismatch noise is **date-independent**, so the collapse on the other side is
a currency signal and not an artifact of it.

**Third check.** Of the 8 (re-)addition dates among the missing sections above,
7 are on or after 2026-08-14. The single exception, `50 CFR 217.90` restored
2026-08-01 and absent, is an upstream ETL miss rather than a currency effect.

2026-08-12 is recorded as the cutoff because it is the latest date for which the
snapshot **demonstrably** reflects the CFR, rather than the midpoint of a bracket
no evidence picks out.

Two localized artifacts do not follow the cutoff and are excluded from it, named
in the registry basis so they are not silently absorbed: `24 CFR 582`/`583` (50
sections removed in 2026-05 that the snapshot retains) and the `48 CFR` removals
of 2026-08-07 (23 of 38 retained — mixed within one title on one date, which a
cutoff cannot produce).

### Why currency still reads `pending` for every provision

Establishing the cutoff exposed a defect in what `stale` meant. It was a
comparison of two scalars — snapshot cutoff against the title's official cutoff —
so promoting the CFR cutoff would have marked **all 217,607** represented
sections `stale`, a 99.3% headline. Measured against the sections' own amendment
dates, only **203 (0.09%)** changed in the 14-day window. The blanket flag
overstates real staleness by roughly **1000x**.

A corpus-level date gap is not per-provision staleness, so `stale` now requires
the provision's own last official amendment date (`official_amendment_date` on
`OfficialProvision`) and abstains to `pending` without it — the project's
"abstain rather than guess" rule applied to currency. The eCFR full-title XML
does not carry that date; supplying it means staging the eCFR versioner
(`/versions/title-{n}.json`) and pinning it as its own oracle input, which is the
next piece of work. The 203 figure above comes from that endpoint but is
**not** yet a pinned input, so it is reported here as evidence and is not used to
classify any provision.

### One defect this investigation found and fixed

Eight sections were reported `missing` because their `[Reserved]` marker had
landed in the **body** rather than the `<HEAD>` the projection reads. eCFR emitted
a degenerate heading holding only the section number and pushed the heading line
down: `49 CFR 1542.5` is `<HEAD>§ 1542.5</HEAD>` with the body `§ 1542.5
[Reserved]`; `2 CFR 700.0` has a real heading and a body of just `[Reserved]`.
All 8 now classify as `reserved`, which moved `missing` 374 → 366 and `reserved`
6,993 → 7,001.

The body test **full-matches** the stripped body and never searches it. A search
would swallow every section whose text merely contains a reserved *subsection* —
`(a) [Reserved] (b) The Administrator shall...` is a section full of law, and
there are thousands — so the pattern requires that the entire body be the marker,
optionally prefixed by the section number the degenerate heading duplicated. That
matches exactly those 8 across all 49 titles and nothing else, and both directions
are covered by parametrized tests.
