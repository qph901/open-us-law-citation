# Text mismatch: code audit and proposed solution

Audit date: 2026-09-10. Application code reviewed at `d765dea`.
Scope: the COV-1A `text_agreement = mismatch` result, its ingestion and
comparison paths, integrity checks, derived artifacts, and downstream citation
offsets. This is a proposal with a reproducible experiment; production behavior
has not been changed.

## Finding

**The dominant problem is duplicated passages inside individual CFR source rows.**
An exact repeated-span removal experiment resolves **62,698 of 63,224 mismatches
(99.1680%)**, with **zero regressions among the 154,383 already matching sections**.
The conservative NFC/whitespace comparison was sufficient once those repeated
passages were removed. Broadening normalization or prioritizing multi-row CFR
assembly would miss the main cause.

Keep the immutable source store. Add a versioned repair candidate and an
independent text-validation artifact. Accept a candidate only with recorded
evidence of agreement; retain unresolved cases explicitly.

## Evidence and measurement

The experiment rehashed both inputs and reproduced every relevant baseline count:

- Dataset: `us_federal_regulations.parquet`, snapshot `v2026.08`, SHA-256
  `6d9bcda025dc9eeeaa1361a8317369899cd87751e4eaa4095049518e611ad26e`.
- Official source: all 49 non-reserved eCFR titles, edition `2026-08-26`, tree hash
  `1f8c4bf7ba7bfec19842e8a4b5959d794afc3b5384577c986639b80d22586ccd`.
- Existing projection: `xml_text_nodes_newline_v2`. Existing normalization:
  `unicode_nfc_whitespace_v1`. Neither was changed for the experiment.
- All 217,607 single-candidate, law-carrying official sections were compared.
  The official denominator stays 219,056. Reserved and heading-only sections
  retain their existing exclusions; the 366 missing and 1,083 multi-row sections
  remain unresolved by this experiment. Federal Register rows are excluded.

| Measurement | Existing source text | With experimental candidates |
|---|---:|---:|
| Sections agreeing after existing normalization | 154,383 | 217,081 |
| Agreement / official law-carrying denominator | 70.4765% | 99.0984% |
| Single-candidate text mismatches | 63,224 | 526 |
| Already matching sections made mismatched | — | 0 |

The original exact-text count remains **133,218**. The new agreement number is a
separate measurement over proposed derived text; it must not overwrite the raw
baseline or be presented as completed COV-1B coverage. It does not establish
currency, citation resolution, table semantics, or fidelity of non-text media.

### What the experiment does

At each run of newline characters, check whether the preceding 390–400
characters exactly equal the following characters, trying the longest first.
Propose removing the newline and second copy, retaining every other character.
Record half-open offsets into the original source. Reject overlapping removal
intervals rather than choosing between conflicting proposals. Compare the result
with the same official projection and normalization as the existing baseline.

Detected repeat lengths in this snapshot are **395–400 characters**, dominated
by 400 and 399. There are 63,068 mismatched sections with a detected seam;
62,698 fully agree after the candidate edit. **56 sections have conflicting
removal intervals and abstain.** Their count is included in the 526 residuals.

For a concrete example, `1 CFR 304.3` has 3,742 normalized source characters
against 3,341 official characters. A 400-character passage appears twice around
a newline. Removing that second copy and separator produces full normalized
agreement. All 61 Title 1 mismatches are explained by this pattern. Title 1 was
the discovery sample; the remaining titles served as an initial validation set.

The observed pattern strongly suggests chunk overlap survived reconstruction
into whole sections. The public upstream chunker explicitly retains overlap;
its configuration defaults to 100 tokens at four characters per token. This
supports the mechanism, but the exact federal export step and historical
configuration that produced this snapshot were not available in the inspected
public code. Causation at that step remains an inference.
[Upstream chunker, pinned commit](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/state_scrapers/vaquill_pipeline/node_to_payload.py#L43-L103),
[configuration](https://github.com/Vaquill-AI/open-us-law/blob/2f7aeb85a434a54a351ac44e3c188fec318f78ba/scripts/state_scrapers/vaquill_pipeline/config.py#L28-L31).

## Code findings, ordered by impact

### 1. High: the integrity model misses the dominant defect

[`text_integrity.py`](../src/open_us_law_citation/text_integrity.py), lines 49–62
and 92–98, checks lowercase starts, amendment banners, and impossible citation
titles. [`derived/quality.py`](../src/open_us_law_citation/derived/quality.py),
lines 70–71, exposes only `duplicate_row`, a relation between whole records.
Neither detects repeated spans within a single row. The baseline correctly
reports inequality at `coverage_baseline.py:540–560`, but cannot explain it.

**Proposed action:** add a within-record integrity annotation and a versioned
repair-candidate producer. Keep these separate from `DuplicateScope`: its
complete-group provenance contract describes a different question. Do not
deduplicate records or change raw hashes.

### 2. High before resolution ships: assembly completion does not verify text

[`derived/assembly.py`](../src/open_us_law_citation/derived/assembly.py), lines
307–325, marks every non-null singleton `complete`, retaining its raw text.
That satisfies the existing composition contract even for repeated or truncated
text. There is no implemented M3 retrieval gate that establishes whole-section
text fidelity. A future consumer must not treat this assembly status alone as
permission to return complete authority.

**Proposed action:** preserve assembly's current meaning and add independent
text validation to retrieval eligibility. Check selected identity, the actual
returned text view, completeness evidence, and requested-edition currency.
Repairing duplication alone cannot supply all of those claims.

### 3. Medium: the official comparison includes amendment notices as body text

[`coverage_baseline.py`](../src/open_us_law_citation/coverage_baseline.py), lines
1097–1121 and 1251–1305, excludes the section heading but flattens every other
text-bearing child. In the pinned XML, `5 CFR 2.3` begins with an
`XREF ID="20260814"` amendment notice. Its remaining 388 normalized characters
equal the entire dataset body; the mismatch is a 62-character notice in the
official projection. `5 CFR 330.202` similarly differs by a correction notice.
This can report a body mismatch even when the body agrees.

**Proposed action:** commission a separate CFR body/notice projection using XML
element context. Retain notices as dated evidence and compare operative text
separately. Match removal of notices from dataset text conservatively, with
recorded spans. Do not drop every `XREF`, bracket, citation, or source credit.
Version any changed projection and regenerate its inventory; retain v2 metrics
for before/after accountability.

The current projector also erases inline and table structure. For example,
`10<SU>2</SU>` becomes `10\n2`; plain text agreement therefore does not prove
that exponents, formulas, and table relationships survived. This experiment
measures the existing string contract only.

### 4. Medium: discrepancy output makes diagnosis difficult

`coverage_baseline.py:718–731` emits candidate identities and coarse statuses,
without comparison hashes, changed spans, or mismatch reasons.
`coverage_baseline.py:935` takes the first discrepancies of any kind; because
currency is pending broadly, all twelve examples in the committed scorecard
are exact text matches. The mismatch population receives no representative
examples in that table.

**Proposed action:** emit deterministic samples by text outcome and reason,
separately from currency. Include source coordinates, oracle coordinates,
before/after hashes, changed intervals, and unresolved reason codes. Also move
snapshot-specific narrative out of the generic renderer: it currently embeds
the 2026-08 counts and date-gap explanation even for other runs.

## Residual cases need separate decisions

The 526 remaining mismatches are an investigation queue, not one defect class.
Examples inspected against the pinned local XML include:

| Example | Observation | Proposed treatment |
|---|---|---|
| `5 CFR 2.3`, `330.202` | Amendment/correction notice differs; body matches | Separate body and notice comparison |
| `5 CFR 575.102` | The dataset includes “less than 6 months or” in a service-period condition where the official edition does not | Preserve mismatch; establish per-section version history |
| `7 CFR 400.766`, `40 CFR 80.1472` | Dataset starts mid-thought and differs substantially | Keep incomplete/unverified; investigate original captures and edition history |
| `40 CFR 63.5984` | `Table` versus `table` | Record case-only difference; retain strict normalization |
| `2 CFR 3485.12` | An authority passage appears additionally in the official projection | Inspect XML structure and body/source-credit policy |
| `10 CFR 429.4` | Repeated-span proposals overlap | Abstain until a separate validated rule resolves the conflict |

The existing corpus cutoff is 2026-08-12, while the oracle edition is
2026-08-26. Pin the provision-level versioner evidence or a second full edition
at the cutoff before assigning stale/aligned outcomes to these cases. A
corpus-level date gap does not prove that an individual provision is stale.
No residual text is reconstructed by guessing missing words or digits.

## Proposed implementation

### First: add explanation and candidate artifacts

Add a narrowly scoped `derived/text_integrity.py` producer and a
`derived/text_repair.py` candidate view, downstream of identity/assembly and
before consumers parse the selected text. This is an explicit extension to the
interpretation layer; it leaves immutable source, identity, and existing assembly
semantics intact. Record the change in `PROPOSAL.md` when implementing it.

Each candidate should carry:

- `DerivedArtifactProvenance`: source record and/or assembly inputs, producer
  version, and a hash of the overlap policy;
- input text hash, candidate text hash, and the standard semantic `payload_hash`;
- ordered removal intervals, exact evidence for both copies, and an output-to-
  source span map;
- a status such as `unchanged`, `candidate`, or `ambiguous`, with reason codes.

The production rule must be frozen and versioned. Do not change
`normalize_legal_text` to remove repetition: repeated legal language can be
intentional. A fixture in this audit demonstrates that the detector alone can
propose an incorrect edit to intentionally repeated text.

### Second: validate the actual returned text independently

Add a `TextValidationAnnotation` naming the source/candidate artifact and the
pinned official edition, **including its source checksum and projection version**
in the derivation inputs/configuration. The edition label alone does not capture
the bytes or projection policy. Store raw agreement and candidate agreement as
separate fields. Candidate acceptance requires complete normalized agreement
under the declared comparison policy, or an explicitly commissioned equivalent
proof; mismatches and unavailable evidence remain unverified.

Candidate generation remains snapshot-internal. Oracle comparison is offline
evaluation/validation with retained artifacts; there is no network dependency at
query time. If official bytes are later adopted as replacement production text,
ingest them as a separate provenanced source through an explicit design change.
Do not silently fill holes in a source record from an oracle.

Update the baseline to report **raw exact**, **raw normalized**, and **validated
repaired normalized** coverage separately. Keep missing, multi-row ambiguity,
currency, and text outcomes orthogonal. Completing CFR-A2 remains necessary for
the 1,083 multi-row sections; it cannot repair the 63,224 singleton mismatches.

### Third: connect text views to parsing and retrieval

`citation_parser.py:330–340` stores character offsets, and
`in_body_detection.py:233–265` currently detects mentions in raw bodies.
Deleting overlap shifts all following offsets. Consumers of repaired text must
name that text view and translate spans through its source map; they must not
reuse repaired offsets as raw offsets. A quote crossing a removed interval maps
to multiple source intervals and must retain that distinction.

Whole-section authority requires separately established identity, faithful text,
and requested-version eligibility. Missing or conflicting evidence yields an
explicit incomplete/unverified outcome with the source link. Re-run the federal
coverage gate after these changes; retain USC anatomy as its own workstream,
since the independent pinned USLM oracle is still unstaged.

## Acceptance criteria and validation performed

Production acceptance should require:

1. Reproduce the raw baseline unchanged and at least the 62,698 demonstrated
   recoveries under this pinned comparison, with zero regressions on its matching
   controls. Review changed spans in a title-, length-, and structure-stratified
   sample; validate on another snapshot before claiming generalization.
2. No accepted edit that loses operative text. Include intentional repetition,
   near-matches with different numbers/negation, conflicting spans, Unicode,
   tables, and truncated prefixes/tails as adversarial fixtures.
3. Preserve every `CanonicalSourceRecord`, `source_record_id`, and `raw_text_hash`.
   Verify source span mapping, deterministic artifacts, version coexistence, and
   the equal-id/unequal-payload tripwire.
4. Never promote an unresolved repair or assembly-only `complete` status to
   verified complete authority. Test currency and text eligibility independently.
5. Preserve the official denominator and publish unresolved strata. Measure
   latency only after the applicable correctness gate passes.

Checks performed in this audit: **495 existing tests passed**; repository lint
and type checks passed. **Four additional audit tests passed**, covering exact
removal/source offsets, unchanged near-matches, conflicting-span abstention, and
the inability of repeated-span detection alone to certify correctness.

The committed measurements are in
[`text_mismatch_experiment.json`](text_mismatch_experiment.json). Reproduce them:

```bash
uv run python scripts/audit_text_mismatch.py \
  --details-output data/audits/text_mismatch_details.jsonl
```

The harness is snapshot-specific and checksum-gated. It scans with DuckDB and
retains one title's dataset bodies at a time, avoiding the known full-row-group
memory failure. It writes aggregate measurements and optional hash/offset
details; it does not persist repaired legal text or alter application behavior.
