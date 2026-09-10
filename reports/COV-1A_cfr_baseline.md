# COV-1A CFR provision coverage baseline

**Status:** preliminary. This is an official-denominator structural/text baseline, not the COV-1B citation-resolution coverage gate.

## Provenance

- Jurisdiction: `US`
- Corpus: `cfr`
- Open US Law snapshot: `v2026.08`
- Open US Law dataset revision: `16bc9a159faabea4af9db08f1b33832e80e85b2d`
- Dataset legal-content cutoff: `2026-08-12` (`established`)
- Official oracle: `oracle:ecfr:point-in-time:2026-08-26`
- Oracle edition date: `2026-08-26`
- Oracle source: `https://www.ecfr.gov/api/versioner/v1/full/2026-08-26/title-{title}.xml`
- Oracle source SHA-256: `1f8c4bf7ba7bfec19842e8a4b5959d794afc3b5384577c986639b80d22586ccd`
- Oracle source hash method: `sha256_tree_v1`
- Normalized inventory SHA-256: `f598213bee35a0690eddcb762f8bac343cbf54f813fc40b4fba7aa78fd8eda52`
- Dataset file: `us_federal_regulations.parquet`
- Dataset file SHA-256: `6d9bcda025dc9eeeaa1361a8317369899cd87751e4eaa4095049518e611ad26e`
- Crosswalk: `canonical_title_section_v1` over `(US, corpus, title, section)`
- Federal Register rows in CFR denominator: **no**

`represented` means exactly one dataset candidate at the official key. Currency and text agreement are separate dimensions; therefore a structurally represented provision can still be stale or text-pending.

`reserved` and `empty_official_body` are **separate strata held out of `expected`**, so every rate below is against sections that carry law. Neither is absent law, so scoring either `missing` would manufacture a coverage gap that does not exist.

A `reserved` section is an explicit empty official placeholder, and eCFR often publishes one element over a whole *range* of numbers (`102.104-102.109`), which is not a key any dataset row could ever match.

An `empty_official_body` section is one the official source publishes as a heading with no body at all. These are overwhelmingly undesignated *parents*: `48 CFR 1.105` is `<HEAD>1.105 Issuance.</HEAD>` and nothing else, because its law lives in `1.105-1`, `1.105-2` and `1.105-3` -- which the dataset does carry. Across the CFR 2026-08-26 edition 1,309 of 1,469 such sections have hyphen-suffixed children in the same official inventory; the remaining 160 are heading-only with no children (43 of them FDA animal-drug sections in title 21). The distinction is drawn from the official bytes, not inferred: the section element's own subtree carries no text.

`missing` is a real gap and is never explained away here. At the CFR 2026-08-26 edition all 366 are accounted for: **291** are bare cross-reference stubs (`See § 1000.3.`), 284 of them in the federal milk marketing orders (title 7, parts 1000-1199), where the snapshot carries the referenced part 1000 in full but none of the sections that incorporate it; **36** sit in two parts the snapshot carries under an older numbering (14 CFR 1216, 50 CFR 20); **15** are terse plain-language answers (`No.`, `60 days.`); **9** have an eCFR amendment banner as their whole body; and **15** carry substantive text that entered the CFR between 2026-08-01 and 2026-08-24, in the four weeks before this edition -- 11 newly added and 4 restored after an earlier removal, each date confirmed against the eCFR versioner. **No missing section is unexplained.** An incorporation by reference is operative law, so the stubs stay `missing` rather than becoming a stratum -- see `COV-1A_status.md`.

Currency reads `pending` for every represented provision even though the snapshot cutoff is established. That is deliberate. The cutoff is a corpus-level date, and a date gap is not per-provision staleness: the CFR snapshot cutoff of 2026-08-12 precedes this 2026-08-26 edition by 14 days, but only **203** of the 217,607 represented sections were actually amended inside that window, so flagging all of them `stale` would overstate real staleness by roughly 1000x. `stale` requires the provision's own last official amendment date, which the eCFR full-title XML does not carry -- it needs the versioner (`/versions/title-{n}.json`) staged and pinned as its own oracle input. Until then currency abstains and the skew is reported here instead.

## Totals

| expected | represented | missing | reserved | empty body | stale | duplicate | ambiguous | unexpected | exact text | normalized text | mismatch | pending text |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 219,056 | 217,607 | 366 | 7,001 | 1,464 | 0 | 232 | 851 | 165 | 133,218 | 154,383 | 63,224 | 1,083 |

Official-denominator rates: **structurally represented 99.3385%**, missing 0.1671%, duplicate 0.1059%, ambiguous 0.3885%, stale 0.0000%, exact text 60.8146%, and normalized text 70.4765%.

Official sections held out of the denominator because they carry no law: **7,001** reserved (`[Reserved]` placeholders) and **1,464** empty-bodied (heading only, no text).

Currency overlays: aligned `0`, stale `0`, ahead of oracle `0`, pending `218,690`, not applicable `531`.

## By title

| title | official cutoff | expected | represented | represented % | missing | reserved | empty body | stale | duplicate | ambiguous | unexpected | exact | normalized | mismatch | pending |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2026-08-26 | 271 | 271 | 100.0000 | 0 | 17 | 0 | 0 | 0 | 0 | 0 | 210 | 210 | 61 | 0 |
| 2 | 2026-08-26 | 1,506 | 1,498 | 99.4688 | 8 | 16 | 0 | 0 | 0 | 0 | 0 | 1,319 | 1,322 | 176 | 0 |
| 3 | 2026-08-26 | 20 | 20 | 100.0000 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 15 | 15 | 5 | 0 |
| 4 | 2026-08-26 | 220 | 220 | 100.0000 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 163 | 163 | 57 | 0 |
| 5 | 2026-08-26 | 5,280 | 5,277 | 99.9432 | 0 | 77 | 0 | 0 | 0 | 3 | 0 | 3,806 | 3,877 | 1,400 | 3 |
| 6 | 2026-08-26 | 578 | 578 | 100.0000 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 372 | 377 | 201 | 0 |
| 7 | 2026-08-26 | 16,243 | 15,881 | 97.7713 | 288 | 961 | 0 | 0 | 0 | 74 | 0 | 9,955 | 12,052 | 3,829 | 74 |
| 8 | 2026-08-26 | 923 | 902 | 97.7248 | 0 | 66 | 0 | 0 | 4 | 17 | 0 | 473 | 475 | 427 | 21 |
| 9 | 2026-08-26 | 2,340 | 2,338 | 99.9145 | 1 | 100 | 0 | 0 | 0 | 1 | 0 | 1,522 | 1,526 | 812 | 1 |
| 10 | 2026-08-26 | 5,151 | 5,117 | 99.3399 | 0 | 114 | 0 | 0 | 6 | 28 | 0 | 3,376 | 3,539 | 1,578 | 34 |
| 11 | 2026-08-26 | 560 | 560 | 100.0000 | 0 | 27 | 0 | 0 | 0 | 0 | 0 | 367 | 367 | 193 | 0 |
| 12 | 2026-08-26 | 6,917 | 6,854 | 99.0892 | 0 | 262 | 0 | 0 | 5 | 58 | 0 | 3,675 | 3,938 | 2,916 | 63 |
| 13 | 2026-08-26 | 1,652 | 1,652 | 100.0000 | 0 | 55 | 0 | 0 | 0 | 0 | 0 | 1,203 | 1,213 | 439 | 0 |
| 14 | 2026-08-26 | 6,204 | 6,172 | 99.4842 | 27 | 154 | 5 | 0 | 1 | 4 | 13 | 4,636 | 4,686 | 1,486 | 5 |
| 15 | 2026-08-26 | 2,173 | 2,151 | 98.9876 | 0 | 64 | 0 | 0 | 5 | 17 | 6 | 1,362 | 1,369 | 782 | 22 |
| 16 | 2026-08-26 | 2,111 | 2,098 | 99.3842 | 0 | 46 | 1 | 0 | 6 | 7 | 0 | 1,369 | 1,378 | 720 | 13 |
| 17 | 2026-08-26 | 3,315 | 3,293 | 99.3363 | 0 | 210 | 0 | 0 | 11 | 11 | 0 | 1,793 | 1,794 | 1,499 | 22 |
| 18 | 2026-08-26 | 2,015 | 2,014 | 99.9504 | 0 | 33 | 0 | 0 | 0 | 1 | 0 | 1,410 | 1,412 | 602 | 1 |
| 19 | 2026-08-26 | 3,097 | 3,095 | 99.9354 | 1 | 75 | 0 | 0 | 0 | 1 | 0 | 2,097 | 2,101 | 994 | 1 |
| 20 | 2026-08-26 | 5,559 | 5,559 | 100.0000 | 0 | 76 | 0 | 0 | 0 | 0 | 0 | 4,137 | 4,148 | 1,411 | 0 |
| 21 | 2026-08-26 | 8,330 | 8,284 | 99.4478 | 2 | 35 | 43 | 0 | 3 | 41 | 0 | 4,373 | 6,133 | 2,151 | 44 |
| 22 | 2026-08-26 | 3,270 | 3,269 | 99.9694 | 0 | 131 | 7 | 0 | 0 | 1 | 0 | 2,496 | 2,498 | 771 | 1 |
| 23 | 2026-08-26 | 974 | 973 | 99.8973 | 0 | 13 | 0 | 0 | 0 | 1 | 4 | 640 | 641 | 332 | 1 |
| 24 | 2026-08-26 | 4,825 | 4,821 | 99.9171 | 1 | 52 | 0 | 0 | 0 | 3 | 50 | 3,295 | 3,301 | 1,520 | 3 |
| 25 | 2026-08-26 | 4,701 | 4,692 | 99.8086 | 9 | 46 | 0 | 0 | 0 | 0 | 0 | 4,206 | 4,206 | 486 | 0 |
| 26 | 2026-08-26 | 6,011 | 6,005 | 99.9002 | 1 | 145 | 0 | 0 | 0 | 5 | 0 | 1,851 | 1,855 | 4,150 | 5 |
| 27 | 2026-08-26 | 3,855 | 3,851 | 99.8962 | 1 | 97 | 0 | 0 | 0 | 3 | 0 | 3,044 | 3,060 | 791 | 3 |
| 28 | 2026-08-26 | 3,001 | 2,987 | 99.5335 | 2 | 70 | 0 | 0 | 4 | 8 | 0 | 2,175 | 2,184 | 803 | 12 |
| 29 | 2026-08-26 | 7,099 | 7,094 | 99.9296 | 1 | 170 | 2 | 0 | 0 | 4 | 0 | 4,923 | 4,947 | 2,147 | 4 |
| 30 | 2026-08-26 | 5,780 | 5,698 | 98.5813 | 0 | 173 | 1 | 0 | 36 | 46 | 0 | 4,514 | 4,739 | 959 | 82 |
| 31 | 2026-08-26 | 5,275 | 5,156 | 97.7441 | 0 | 167 | 0 | 0 | 61 | 58 | 0 | 4,015 | 4,232 | 924 | 119 |
| 32 | 2026-08-26 | 3,588 | 3,581 | 99.8049 | 0 | 52 | 0 | 0 | 3 | 4 | 0 | 2,528 | 2,530 | 1,051 | 7 |
| 33 | 2026-08-26 | 4,594 | 4,590 | 99.9129 | 2 | 55 | 0 | 0 | 0 | 2 | 0 | 3,533 | 3,545 | 1,045 | 2 |
| 34 | 2026-08-26 | 3,138 | 3,127 | 99.6495 | 0 | 121 | 0 | 0 | 0 | 11 | 0 | 2,218 | 2,229 | 898 | 11 |
| 36 | 2026-08-26 | 3,054 | 3,054 | 100.0000 | 0 | 81 | 0 | 0 | 0 | 0 | 0 | 2,246 | 2,248 | 806 | 0 |
| 37 | 2026-08-26 | 1,256 | 1,254 | 99.8408 | 0 | 75 | 0 | 0 | 0 | 2 | 0 | 708 | 759 | 495 | 2 |
| 38 | 2026-08-26 | 2,863 | 2,852 | 99.6158 | 0 | 99 | 0 | 0 | 4 | 7 | 0 | 1,738 | 1,743 | 1,109 | 11 |
| 39 | 2026-08-26 | 1,119 | 1,117 | 99.8213 | 0 | 18 | 0 | 0 | 0 | 2 | 0 | 861 | 883 | 234 | 2 |
| 40 | 2026-08-26 | 23,362 | 23,328 | 99.8545 | 5 | 1,245 | 43 | 0 | 2 | 27 | 0 | 2,681 | 14,540 | 8,788 | 29 |
| 41 | 2026-08-26 | 2,934 | 2,934 | 100.0000 | 0 | 82 | 78 | 0 | 0 | 0 | 0 | 2,553 | 2,568 | 366 | 0 |
| 42 | 2026-08-26 | 7,219 | 7,203 | 99.7784 | 1 | 68 | 3 | 0 | 0 | 15 | 0 | 4,689 | 4,724 | 2,479 | 15 |
| 43 | 2026-08-26 | 5,193 | 5,177 | 99.6919 | 1 | 47 | 196 | 0 | 7 | 8 | 0 | 4,334 | 4,349 | 828 | 15 |
| 44 | 2026-08-26 | 901 | 900 | 99.8890 | 0 | 42 | 0 | 0 | 0 | 1 | 0 | 618 | 618 | 282 | 1 |
| 45 | 2026-08-26 | 5,631 | 5,629 | 99.9645 | 0 | 186 | 0 | 0 | 0 | 2 | 47 | 3,939 | 4,062 | 1,567 | 2 |
| 46 | 2026-08-26 | 8,335 | 8,304 | 99.6281 | 0 | 110 | 0 | 0 | 23 | 8 | 0 | 6,879 | 6,910 | 1,394 | 31 |
| 47 | 2026-08-26 | 4,719 | 4,593 | 97.3299 | 1 | 459 | 0 | 0 | 17 | 108 | 11 | 2,374 | 3,000 | 1,593 | 125 |
| 48 | 2026-08-26 | 10,116 | 10,007 | 98.9225 | 1 | 378 | 1,056 | 0 | 3 | 105 | 23 | 5,556 | 8,120 | 1,887 | 108 |
| 49 | 2026-08-26 | 8,706 | 8,580 | 98.5527 | 1 | 275 | 29 | 0 | 23 | 102 | 0 | 5,226 | 6,034 | 2,546 | 125 |
| 50 | 2026-08-26 | 3,072 | 2,997 | 97.5586 | 12 | 141 | 0 | 0 | 8 | 55 | 11 | 1,745 | 1,763 | 1,234 | 63 |

## Deterministic discrepancy sample

| provision | structural | currency | text | candidates |
|---|---|---|---|---:|
| `us:cfr:1:1.1` | represented | pending | exact | 1 |
| `us:cfr:1:2.1` | represented | pending | exact | 1 |
| `us:cfr:1:2.2` | represented | pending | exact | 1 |
| `us:cfr:1:2.3` | represented | pending | exact | 1 |
| `us:cfr:1:2.4` | represented | pending | exact | 1 |
| `us:cfr:1:2.5` | represented | pending | exact | 1 |
| `us:cfr:1:2.6` | represented | pending | exact | 1 |
| `us:cfr:1:3.1` | represented | pending | exact | 1 |
| `us:cfr:1:3.2` | represented | pending | exact | 1 |
| `us:cfr:1:3.3` | represented | pending | exact | 1 |
| `us:cfr:1:5.1` | represented | pending | exact | 1 |
| `us:cfr:1:5.2` | represented | pending | exact | 1 |

## Unmatched official examples

- `us:cfr:2:200.506` (cfr-title-2-section-200.506)
- `us:cfr:2:910.200` (cfr-title-2-section-910.200)
- `us:cfr:2:910.210` (cfr-title-2-section-910.210)
- `us:cfr:2:910.230` (cfr-title-2-section-910.230)
- `us:cfr:2:910.240` (cfr-title-2-section-910.240)
- `us:cfr:2:910.250` (cfr-title-2-section-910.250)
- `us:cfr:2:910.260` (cfr-title-2-section-910.260)
- `us:cfr:2:910.270` (cfr-title-2-section-910.270)
- `us:cfr:7:58.647` (cfr-title-7-section-58.647)
- `us:cfr:7:58.652` (cfr-title-7-section-58.652)
- `us:cfr:7:984.348` (cfr-title-7-section-984.348)
- `us:cfr:7:984.349` (cfr-title-7-section-984.349)

## Dataset-only examples

- `us:cfr:14:1216.102` (CFR_T14_P1216_S1216_102)
- `us:cfr:14:1216.103` (CFR_T14_P1216_S1216_103)
- `us:cfr:14:1216.301` (CFR_T14_P1216_S1216_301)
- `us:cfr:14:1216.302` (CFR_T14_P1216_S1216_302)
- `us:cfr:14:1216.303` (CFR_T14_P1216_S1216_303)
- `us:cfr:14:1216.304` (CFR_T14_P1216_S1216_304)
- `us:cfr:14:1216.305` (CFR_T14_P1216_S1216_305)
- `us:cfr:14:1216.306` (CFR_T14_P1216_S1216_306)
- `us:cfr:14:1216.307` (CFR_T14_P1216_S1216_307)
- `us:cfr:14:1216.308` (CFR_T14_P1216_S1216_308)
- `us:cfr:14:1216.309` (CFR_T14_P1216_S1216_309)
- `us:cfr:14:1216.310` (CFR_T14_P1216_S1216_310)

## Federal Register separation

Excluded `362,036` Federal Register rows from the codified-CFR denominator. They are promulgation-record inventory and require a separate report.
