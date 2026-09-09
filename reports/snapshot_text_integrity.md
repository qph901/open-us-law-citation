# Snapshot text integrity

Snapshot: `v2026.08`. Does a row's `text` hold the whole provision? A supporting
audit, not a chartered milestone, and one that needs **no official oracle** — every
defect below is detectable from the snapshot alone.

## Defect rates

| file | rows | non-null text | truncated head | UI chrome | impossible-title citation |
|---|---:|---:|---:|---:|---:|
| us_federal_regulations | 582,054 | 582,054 | 8,011 (1.38%) | 906 | 3,172 |
| us_federal_statutes | 54,853 | 54,853 | 1 (0.00%) | 0 | 17 |

`truncated head` = the body begins with a lowercase letter, i.e. mid-word. `UI chrome` = the body carries the eCFR banner `Link to an amendment published…`, website furniture captured as legal text. `impossible-title citation` = a digit run adjacent to a code token straight after a newline (`\n0 CFR 264.100`, really 40 CFR).

## Damage that reached the extracted fields

Rows whose own `cross_references_usc` names a US Code title that does not exist (outside 1-54) — the corruption propagating out of the text into the dataset's structured columns.

| file | rows with an impossible cross-reference title |
|---|---:|
| us_federal_regulations | 0 |
| us_federal_statutes | 1 |

## Samples — us_federal_regulations

Truncated heads (each begins mid-word):

- `CFR_T10_P10_S10_11` — `ited States or any State or any subdivisions thereof by unlawful means, or which advocat…`
- `CFR_T10_P26_S26_205` — `al evolutions; and holdovers for interviews needed for event investigations. (2) Within-…`
- `CFR_T10_P2_S2_202` — `ublic health, safety, or interest so requires or that the violation or conduct causing t…`
- `CFR_T10_P2_S2_202` — `e requirements, the requirements of § 52.63 of this chapter must be followed, unless the…`
- `CFR_T10_P2_S2_390` — `piled by a criminal law enforcement authority in the course of a criminal investigation,…`
- `CFR_T10_P31_S31_5` — `ng the radioactive materials, its shielding or containment, are performed: (i) In accord…`
- `CFR_T10_P51_S51_4` — `and transmission lines);
(H) Procurement or fabrication of components or portions of the…`
- `CFR_T10_P54_S54_17` — `possess Restricted Data or classified National Security Information until the individual…`

UI chrome in the body:

- `CFR_T10_P1040_S1040_1` — `Link to an amendment published at 90 FR 20782, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_102` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_12` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_13` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_14` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_5` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_6` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`
- `CFR_T10_P1040_S1040_72` — `Link to an amendment published at 90 FR 20783, May 16, 2025. This amendment was delayed …`

## Samples — us_federal_statutes

Truncated heads (each begins mid-word):

- `USC_T15_C2A_S77aa` — `schedule a

(1) The name under which the issuer is doing or intends to do business;

(2)…`

## Why this is a coverage question, not a tidiness question

COV-1A scores a provision `represented` when exactly one dataset row sits at the official
key. That test is **structural**: it asks whether a row exists, never whether the row holds
the whole provision. A truncated body passes it. So the represented rate and the truncation
rate are independent, and a coverage number quoted without the second is an overstatement of
what the corpus can actually answer with.

Text agreement (COV-1A's third dimension) would catch these — but only once the official
oracle is staged and only where the comparison is not `pending`. This audit needs no oracle
at all, so it is available now and stays available for every corpus that has no oracle.

## What the truncation signal is, and is not

The detector is deliberately blunt: the first non-space character of the body is a lowercase
letter. Sampled, it is overwhelmingly genuine mid-word truncation — `'ited States or any
State…'`, `'ublic health, safety, or interest…'`, `'piled by a criminal law enforcement
authority…'`, `'ewed Amendment Number 4…'` — but it is a proxy, not a proof, and a body that
legitimately opens on a lowercase word would be counted. Read the rate with that in view;
the samples below are provided so it can be judged rather than taken on trust.

The converse error is invisible here: a body truncated at a **word boundary** ("United
States or any State…" with an earlier paragraph missing) reads as a clean start and is not
counted. **The measured rate is therefore a lower bound on truncation.**

## Cross-check against CFR-A1

Several `act_id`s counted here as truncated are ones `reports/CFR-A1_commissioning_frame.md`
classified `candidate_segmented` — the stratum whose rows show a mid-thought continuation
seam. That overlap matters for CFR-A2: a "continuation" seam between two rows is equally
consistent with **one row being a truncated capture** as with the two being ordered segments
of one section. It is further evidence for the selection-over-composition respecification —
concatenating a truncated capture to its sibling does not reconstruct the section, it
splices across a hole — and it means the 31 `candidate_segmented` groups need the eCFR
comparison before any of them is treated as composable.

