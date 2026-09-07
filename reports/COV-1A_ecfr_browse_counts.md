# COV-1A preflight — official eCFR section denominators

**Status:** preflight cross-check, not a coverage report. These are official
per-title section *counts* from the eCFR **point-in-time** structure API at the
pinned comparison date `2026-08-26` — the browse denominator against which the real
CFR crosswalk will be validated once the point-in-time eCFR bytes are staged and
checksum-pinned. No coverage percentage is asserted here.

## Method

- Source: `https://www.ecfr.gov/api/versioner/v1/structure/2026-08-26/title-{n}.json`
  (structure only — no regulatory text is fetched or retained).
- A *section* is a node with `type == "section"`; `reserved` is the API's own flag.
- **Active = total − reserved.** Reserved sections are legally empty placeholders.
- Point-in-time, not `/current/`: the counts are reproducible for this date.
- Title inventory from `/versioner/v1/titles.json`: 50 titles, title 35 reserved.

## Per-title section counts (as of 2026-08-26)

| Title | Name | Total | Reserved | Active |
|---:|---|---:|---:|---:|
| 1 | General Provisions | 288 | 17 | 271 |
| 2 | Federal Financial Assistance | 1,522 | 15 | 1,507 |
| 3 | The President | 27 | 7 | 20 |
| 4 | Accounts | 222 | 2 | 220 |
| 5 | Administrative Personnel | 5,357 | 77 | 5,280 |
| 6 | Domestic Security | 584 | 6 | 578 |
| 7 | Agriculture | 17,204 | 960 | 16,244 |
| 8 | Aliens and Nationality | 989 | 66 | 923 |
| 9 | Animals and Animal Products | 2,440 | 100 | 2,340 |
| 10 | Energy | 5,265 | 114 | 5,151 |
| 11 | Federal Elections | 587 | 27 | 560 |
| 12 | Banks and Banking | 7,179 | 262 | 6,917 |
| 13 | Business Credit and Assistance | 1,707 | 55 | 1,652 |
| 14 | Aeronautics and Space | 6,363 | 153 | 6,210 |
| 15 | Commerce and Foreign Trade | 2,237 | 64 | 2,173 |
| 16 | Commercial Practices | 2,158 | 46 | 2,112 |
| 17 | Commodity and Securities Exchanges | 3,525 | 210 | 3,315 |
| 18 | Conservation of Power and Water Resources | 2,048 | 33 | 2,015 |
| 19 | Customs Duties | 3,172 | 75 | 3,097 |
| 20 | Employees' Benefits | 5,635 | 76 | 5,559 |
| 21 | Food and Drugs | 8,408 | 35 | 8,373 |
| 22 | Foreign Relations | 3,408 | 131 | 3,277 |
| 23 | Highways | 987 | 12 | 975 |
| 24 | Housing and Urban Development | 4,877 | 52 | 4,825 |
| 25 | Indians | 4,747 | 46 | 4,701 |
| 26 | Internal Revenue | 6,156 | 145 | 6,011 |
| 27 | Alcohol, Tobacco Products and Firearms | 3,952 | 97 | 3,855 |
| 28 | Judicial Administration | 3,071 | 70 | 3,001 |
| 29 | Labor | 7,271 | 170 | 7,101 |
| 30 | Mineral Resources | 5,954 | 173 | 5,781 |
| 31 | Money and Finance: Treasury | 5,442 | 166 | 5,276 |
| 32 | National Defense | 3,640 | 52 | 3,588 |
| 33 | Navigation and Navigable Waters | 4,649 | 54 | 4,595 |
| 34 | Education | 3,259 | 121 | 3,138 |
| 35 | Reserved | — | — | — (title reserved; no structure) |
| 36 | Parks, Forests, and Public Property | 3,135 | 81 | 3,054 |
| 37 | Patents, Trademarks, and Copyrights | 1,331 | 75 | 1,256 |
| 38 | Pensions, Bonuses, and Veterans' Relief | 2,962 | 99 | 2,863 |
| 39 | Postal Service | 1,137 | 18 | 1,119 |
| 40 | Protection of Environment | 24,650 | 1,245 | 23,405 |
| 41 | Public Contracts and Property Management | 3,094 | 82 | 3,012 |
| 42 | Public Health | 7,290 | 68 | 7,222 |
| 43 | Public Lands: Interior | 5,436 | 47 | 5,389 |
| 44 | Emergency Management and Assistance | 943 | 42 | 901 |
| 45 | Public Welfare | 5,817 | 186 | 5,631 |
| 46 | Shipping | 8,445 | 110 | 8,335 |
| 47 | Telecommunication | 5,178 | 458 | 4,720 |
| 48 | Federal Acquisition Regulations System | 11,550 | 376 | 11,174 |
| 49 | Transportation | 9,010 | 268 | 8,742 |
| 50 | Wildlife and Fisheries | 3,213 | 141 | 3,072 |
| | **Total (49 titles)** | **227,521** | **6,985** | **220,536** |

Title 35 is reserved in its entirety; the structure endpoint returns no document
for it, consistent with `titles.json` marking it `reserved`.

## Denominator finding (the reason this preflight matters)

- Official **active** sections: **220,536**. Official **total** (incl. reserved): **227,521**.
- The snapshot carries **220,018** eCFR-linked CFR rows (per corpus reconnaissance;
  the 362,036 Federal Register rows are excluded from the codified-CFR denominator).
- The snapshot row count tracks the **active** denominator (220,018 vs 220,536;
  Δ=518, 0.23%), **not** the total.
- But `coverage_baseline._ecfr_provisions` currently projects **every** `TYPE="section"`
  element without filtering reserved, so its denominator would be ~the **total**
  (227,521). Scored naively, the ~6,985 reserved sections would surface as
  `missing` — which is wrong: a reserved section is legally empty, not absent law.

**Design consequence (for the real crosswalk, once eCFR is pinned):** reserved
sections must be a distinct stratum, not `missing`. Either the projection filters
`reserved` out of the denominator, or the crosswalk classifies a reserved official
key as its own outcome. This is a count-level denominator check only — equal totals
would not prove the *right* sections are present (missing and unexpected can cancel);
that requires the provision-level crosswalk against the pinned point-in-time bytes.

