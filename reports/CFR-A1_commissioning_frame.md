# CFR-A1 — CFR assembly commissioning frame (snapshot-internal half)

Snapshot: `v2026.08`. Every multi-row `CFR_*` `act_id` group in
`us_federal_regulations`, classified by the physical relationship between its rows.

**This is the half of CFR-A1 that needs no oracle.** The validation half — comparing
a proposed assembly against the point-in-time eCFR edition that is COV-1A's
denominator — is pending those bytes. Accordingly this emits **no**
`SourceDocumentAssembly` and marks nothing `complete`: CFR-A2 stays gated.

## Population

- CFR rows: **220,018**; distinct `act_id`: **218,865**
- Multi-row groups: **1,083** covering **2,236** rows (0.5% of distinct sections)

## Group relations

| relation | groups | share | meaning for assembly |
|---|---:|---:|---|
| `duplicate_only` | 232 | 21.4% | every row byte-identical — dedup is an identity, no composition needed |
| `variant_capture` | 376 | 34.7% | overlapping renderings of one section — **concatenation would duplicate text** |
| `candidate_segmented` | 31 | 2.9% | disjoint rows with a mid-thought continuation seam — the only composer candidates |
| `undetermined` | 444 | 41.0% | no evidence either way — abstain |

Groups containing a wholly-contained pair: **365**. Groups with any continuation seam: **34**.

## Overlap distribution (non-duplicate groups)

Max shared prefix/suffix between any pair, as a fraction of the shorter row.

| band | groups | share |
|---|---:|---:|
| `[0.00, 0.01)` | 326 | 38.3% |
| `[0.01, 0.05)` | 45 | 5.3% |
| `[0.05, 0.15)` | 54 | 6.3% |
| `[0.15, 0.30)` | 36 | 4.2% |
| `[0.30, 0.50)` | 16 | 1.9% |
| `[0.50, 0.90)` | 11 | 1.3% |
| `[0.90, 1.01)` | 363 | 42.7% |

## Group sizes

| rows in group | groups |
|---:|---:|
| 2 | 1,016 |
| 3 | 64 |
| 4 | 3 |

## Deterministic commissioning sample

The first 12 groups of each stratum by `act_id` — a stable frame
for the eCFR validation half to draw from, so that run is reproducible rather than
re-sampled.

**`duplicate_only`**

- `CFR_T10_P10_S10_1` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P205_S205_300` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P20_S20_2201` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P429_S429_37` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P50_S50_30` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P53_S53_1100` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T12_P701_S701_26` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T12_P741_S741_10` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T12_P741_S741_203` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T12_P741_S741_5` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T12_P746_S746_201` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T14_P1250_S1250_103_2` — 2 rows, overlap 1.000, continuation 0/1

**`variant_capture`**

- `CFR_T10_P140_S140_20` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P171_S171_15` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P171_S171_16` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P20_S20_1003` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P25_S25_17` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P2_S2_340` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P50_S50_54` — 3 rows, overlap 1.000, continuation 0/2
- `CFR_T10_P51_S51_22` — 3 rows, overlap 1.000, continuation 0/2
- `CFR_T10_P52_S52_39` — 2 rows, overlap 1.000, continuation 0/1
- `CFR_T10_P54_S54_17` — 3 rows, overlap 1.000, continuation 0/2
- `CFR_T10_P70_S70_72` — 3 rows, overlap 1.000, continuation 0/2
- `CFR_T10_P72_S72_32` — 2 rows, overlap 1.000, continuation 0/1

**`candidate_segmented`**

- `CFR_T10_P2_S2_202` — 3 rows, overlap 0.001, continuation 1/2
- `CFR_T10_P2_S2_390` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T10_P51_S51_4` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T10_P70_S70_22` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T10_P72_S72_214` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T12_P701_S701_25` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T15_P758_S758_10` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T15_P8_S8_4` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T21_P201_S201_327` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T26_P20_S20_2056A_4` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T30_P250_S250_1202` — 2 rows, overlap 0.000, continuation 1/1
- `CFR_T30_P250_S250_1203` — 2 rows, overlap 0.000, continuation 1/1

**`undetermined`**

- `CFR_T10_P10_S10_11` — 2 rows, overlap 0.115, continuation 0/1
- `CFR_T10_P170_S170_31` — 2 rows, overlap 0.000, continuation 0/1
- `CFR_T10_P26_S26_205` — 2 rows, overlap 0.000, continuation 0/1
- `CFR_T10_P2_S2_804` — 2 rows, overlap 0.030, continuation 0/1
- `CFR_T10_P31_S31_5` — 2 rows, overlap 0.000, continuation 0/1
- `CFR_T10_P73_S73_55` — 2 rows, overlap 0.000, continuation 0/1
- `CFR_T10_P73_S73_56` — 2 rows, overlap 0.000, continuation 0/1
- `CFR_T10_P75_S75_4` — 2 rows, overlap 0.001, continuation 0/1
- `CFR_T12_P1002_S1002_15` — 2 rows, overlap 0.000, continuation 0/1
- `CFR_T12_P1002_S1002_6` — 2 rows, overlap 0.000, continuation 0/1
- `CFR_T12_P1002_S1002_8` — 2 rows, overlap 0.000, continuation 0/1
- `CFR_T12_P191_S191_5` — 2 rows, overlap 0.297, continuation 0/1

## What this changes about CFR-A2

**Concatenation is the wrong primitive for this corpus.** CFR-A2 is specified as a
composer -- "continuation signal + physical row order + dedup" -- but only **34 of 1,083**
multi-row groups (3.1%) contain even one seam where a row stops mid-thought and the next
resumes it, and 2 of those also contain a wholly-contained pair, which is evidence against
segmentation rather than for it. A concatenating producer would therefore apply to at most
~3% of multi-row groups, i.e. ~0.014% of the 218,865 distinct CFR sections.

The dominant real phenomenon is different: **376 groups (34.7%) are variant captures** --
two renderings of the same section, one typically carrying an eCFR amendment banner
("Link to an amendment published...") or truncated mid-word, with 365 of them containing a
pair where one row's text sits **wholly inside** another's. Concatenating such a pair does
not reconstruct a section; it emits the operative text twice under a whole-section
citation. That is the failure CFR-A1 has zero tolerance for, and it is the *majority*
outcome among non-duplicate groups -- so the composer must be able to recognise and refuse
it, not merely order rows.

This is the same shape of negative result M0.5A.1 established for `FR_*`, arrived at
independently: co-numbered rows are mostly not ordered pieces of one document.

## The threshold is calibrated, not asserted

Overlap is bimodal across the 851 non-duplicate groups -- 38.3% sit below 0.01 and 42.7%
at or above 0.90, with only 3.2% in the whole 0.30-0.90 band. The 0.50 cut therefore falls
in an empty valley: moving it anywhere inside that band reclassifies almost nothing. Where
evidence is genuinely weak the classifier falls through to `undetermined`, which abstains.

## Decision B depends on a choice this spike cannot make alone

PROPOSAL.md decision B reconsiders the build-time eCFR dependency if CFR-A1 **abstains on
more than 50% of multi-row CFR groups**. That number is not single-valued here -- it turns
on whether *superset selection* is permitted:

- **Abstain on everything not provably safe** (only all-identical groups resolve): **78.6%**
  (851 of 1,083) -- above the 50% trigger.
- **Also allow superset selection** where one row's text wholly contains another's, taking
  the containing row: **44.9%** (486 of 1,083) -- below the trigger.

Superset selection is provably never *partial relative to the group's own members*: the
containing row holds every byte the contained row held, so nothing is dropped. It is **not**
proof of completeness against the official section -- the containing row may itself be
truncated, which only the pinned eCFR edition can settle. The recommendation is therefore
to treat superset selection as a candidate CFR-A2 rule whose `complete` claim stays gated
on the eCFR half of CFR-A1, and to read 78.6% as the abstention rate that holds until then.

## What is NOT established here

This harness is snapshot-internal by construction and emits **no** `SourceDocumentAssembly`.
It cannot report continuation-classification precision/recall, assembled-text match, or the
partial-law rate: every one of those compares a proposed assembly against the point-in-time
eCFR edition, which is not yet staged. `candidate_segmented` means *the snapshot shows a
continuation signal*, never *these rows are the pieces of this section*.

