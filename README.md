# Open US Law Citation

A foundation for reliable legal citations: identify the intended provision,
retrieve faithful text from a specified version, and preserve source evidence
with explicit uncertainty where a reference cannot be resolved.

The current implementation builds a date-pinned law inventory and retrieval system over the
[`vaquill/open-us-law`](https://huggingface.co/datasets/vaquill/open-us-law)
dataset (snapshot **v2026.08**), federally commissioned against official USC and
CFR inventories. Citation parsing and resolution remain correctness capabilities
inside that system. See
[PROPOSAL.md](PROPOSAL.md) for the full design and milestones. Project decisions
are ordered by [PRIORITIES.md](PRIORITIES.md): law coverage first, retrieval time
second. Coverage measures how broadly the system can provide reliable citations;
the existing milestone order and acceptance criteria remain in effect.

## Status

- **M0 — Dataset reconnaissance: complete.** Report at
  [reports/M0_recon.md](reports/M0_recon.md). Answers the proposal's `act_id`
  behavior, crosswalk-field, hierarchy-cleanliness, and citation-format
  questions against real Parquet (deterministic renumber lineage from text;
  breadcrumb-based hierarchy; pre-extracted USC cross-references).
- **M0 — Full-snapshot reconnaissance: complete.** Report at
  [reports/M0_full_snapshot.md](reports/M0_full_snapshot.md). The recon harness
  run over all **229 files / 2,978,617 rows** of `v2026.08`: one uniform
  24-column schema everywhere, no crosswalk column anywhere, `act_id` 100%
  populated across every corpus (but **not unique within the federal
  regulations file** — a Tier-1 caveat), and 10,395 rows carrying a
  disposition status that routes to lineage inference. Confirms the sample-set
  findings hold at full scale.
- **M0 — `act_id` stability across snapshots: answered.** Report at
  [reports/M0_act_id_stability.md](reports/M0_act_id_stability.md). Diffing
  `v2026.07` → `v2026.08` across federal/CA/AK: **no act_id was ever removed or
  reissued**, and thousands survive text amendment → `act_id` is a safe Tier-1
  identity seed. Key caveat: the USC `text` field bundles a volatile
  editorial-notes apparatus, so `text_hash` over raw `text` overstates real
  amendment (~48% of USC "changed", almost all editorial-note growth). Hash the
  operative body separately.
- **M0.5A — Identity-collision analysis: complete.** Report at
  [reports/M0.5A_identity_collisions.md](reports/M0.5A_identity_collisions.md).
  Collisions are **entirely a regulations-corpus phenomenon** (7 of 229 files;
  every statute/constitution `act_id` is unique). In `us_federal_regulations`
  the file mixes two namespaces: `CFR_*` (codified sections, ~nearly unique) and
  `FR_*` (Federal Register documents split into text segments — 99.99% of the
  167k collision rows). State-regulation collisions are mostly literal duplicate
  rows (Ohio: 539/555 groups byte-identical). Yields a per-corpus
  `SourceIdentityStrategy`: `source_id = (state, corpus, act_id, segment_ordinal)`
  for regulations, `legal_id = (state, corpus, act_id)` at document/section
  granularity, duplicate rows flagged not silently deduped.
- **M0.5A.1 — Collision-provenance + segment-order spike: complete.** Report at
  [reports/M0.5A1_segment_provenance.md](reports/M0.5A1_segment_provenance.md).
  Two findings reshape M0.5A. (1) The v2026.07↔v2026.08 comparison A.1 called for
  has an **empty domain** — regulations were *introduced* in v2026.08, so exit
  questions on cross-snapshot segment/order stability are **untestable** until a
  second regulations-bearing snapshot ships. (2) The `FR_*` distinct-text
  collisions are **co-numbered distinct documents, not ordered segments**: their
  rows are physically scattered, the continuation rate is ≈0%, and ≈96% of groups
  restart with the same agency preamble — so concatenating them reconstructs
  nothing. Conclusion: `segment_ordinal` is **snapshot-observed physical row
  order** (no source-defined ordinal exists), a lossless row discriminator only,
  never a reading order. The source-identity contract may freeze with that caveat.
- **M1A — immutable `CanonicalSourceRecord` core: complete.** Lossless
  serializer in
  [`src/open_us_law_citation/source_record.py`](src/open_us_law_citation/source_record.py),
  with the golden-fixture acceptance suite in
  [`tests/test_source_record.py`](tests/test_source_record.py) (21 invariants,
  incl. the **boundary test**: a simulated identity/anatomy/hierarchy/quality
  parser improvement requires *zero* changes to any source record). Preserves all
  24 columns verbatim (null stays null), holds `raw_text` byte-for-byte, and
  derives `source_record_id` from physical coordinates only —
  `(snapshot_version, source_file_checksum, physical_row_ordinal)` — never from
  content or citation. The reader stays row-group-bounded, so a full-snapshot
  pass is safe on the 11 GB federal regulations `text` column. Run:
  `uv run pytest`.
- **M1A.5 — shared derived-artifact foundation: closed, with concrete identity
  producers.** The interpretation-layer contracts in
  [`src/open_us_law_citation/derived/`](src/open_us_law_citation/derived/):
  `DerivedArtifactProvenance` as a multi-input DAG (`artifact_id` is the stable
  derivation address, `generated_at` excluded) **plus a `payload_hash` semantic content
  address and the equal-id/unequal-payload tripwire**; identity as a
  `SourceIdentityGroup` (content-addressed by the complete member set) + per-member
  `SourceIdentityMemberAnnotation` (the `DuplicateScope` analogue — groups only,
  never composes); deterministic `DocumentClassificationAnnotation`,
  `duplicate_row`-only `QualityAnnotation`, and `trivial_single_record_v2`
  `SourceDocumentAssembly`. Every model rejects malformed direct construction.
  The **concrete `SourceIdentityStrategy` producers** are built
  (`usc_act_id_v1` / `state_statute_act_id_v1` / `constitution_act_id_v1` and the
  regulations collision strategies `cfr_identity_v1` / `federal_register_document_v1`),
  and the headline **durable-FK test** runs against real producer outputs
  (v1↔v2 coexist over the same records; a membership change re-hashes the group and
  every member; no artifact keyed by `source_identity_key`). Full-snapshot identity
  manifest at [reports/M1A5_identity_manifest.md](reports/M1A5_identity_manifest.md).
  The CFR multi-row producer (`cfr_source_selection_v1`) lands in CFR-A2 — respecified
  from composition to **selection** on CFR-A1 evidence.
- **M0.5B2 — Hierarchy stress test: complete.** Report at
  [reports/M0.5B2_hierarchy.md](reports/M0.5B2_hierarchy.md). A single
  `breadcrumb`-driven parser normalizes CA statutes (variable code/division/part/
  title ordering), TX statutes (flat, `title_number` 100% null), OH regulations
  (agency/chapter/rule), and DE regulations (title/group/regulation with
  *unnumbered container* nodes) into one `HierarchyNode[]` shape — **no interface
  change forced**. Topology tested, not just coverage: acyclicity and proper-tree
  assembly are clean, but **bare-identifier LOCAL resolution is unsafe** (12–26%
  of leaf `(kind,identifier)` keys sit under >1 parent) and **sibling order is
  only partly recoverable** from physical row order (8–90% by corpus), so
  RELATIVE resolution must operate on the absolute path and abstain on the rest.
- **M0.5B3 — CA abstraction-falsification probe: complete.** Report at
  [reports/M0.5B3_ca_abstraction.md](reports/M0.5B3_ca_abstraction.md). Runs every
  built artifact type over the full 161,566-row CA statutes corpus: **zero
  interface changes forced** — identity is 1:1 (`act_id` and `StructuralPath` both
  100% unique), classification/hierarchy/assembly all represent CA without
  distortion. Two requirements captured as *producer/taxonomy* notes: `duplicate_row`
  must be scoped to the identity group (CA has 7,642 rows byte-identical across
  *distinct* provisions — content ≠ identity), and anatomy (B1) must carry a
  leading `[Repealed … and added by Stats. …]` history bracket and not trust
  `act_status`. **M0.5B1 (needs USLM) / CFR-A1 (needs eCFR): not started.**
- **COV-1A — official federal provision baseline: in progress.** The first
  buildable slice is in
  [`src/open_us_law_citation/coverage_baseline.py`](src/open_us_law_citation/coverage_baseline.py):
  checksum-gated USLM/eCFR provision inventories, deterministic zero/one/multiple
  crosswalks, separate structural/currency/text outcomes, explicit Federal
  Register exclusion, and byte-stable JSON/Markdown output. The implementation
  status and metric definitions are in
  [`reports/COV-1A_status.md`](reports/COV-1A_status.md). Real USC/CFR scorecards
  remain pending until the complete official bytes are staged and pinned; no row
  count is presented as coverage.
- **M2 — federal exact-citation parser (oracle-independent slice): started.**
  [`src/open_us_law_citation/citation_parser.py`](src/open_us_law_citation/citation_parser.py):
  a deterministic USC/CFR citation grammar (`usc_grammar_v1` / `cfr_grammar_v3`) →
  structured `ParsedCitation` / `ReferenceMention` (pre-resolution; provenance on the
  interpretation boundary). Resolution (M3), the alias index, and official validation are
  out of scope. Started ahead of the M1B freeze because the parser needs no blocked
  oracle bytes: the dataset's own `citation`/`citation_short` + structured
  `title_number`/`section_number` are a full-corpus labeled set. Self-check at
  [`reports/M2_parse_selfcheck.md`](reports/M2_parse_selfcheck.md) — **USC 100.00%
  exact**, **CFR 100.00% with 0 mismatches** (the parser also recovers `title_number`
  where the flat column is null, and parses 14 CFR Part 241's dotless sections with no
  part at reduced confidence); the only 6 remaining CFR rows are malformed source
  citations, where abstaining is the correct outcome. Stage-A **detection** is measured
  separately on a hand-labelled gold set (36 passages incl. adversarial distractors) in
  [`reports/M2_detection_metrics.md`](reports/M2_detection_metrics.md) — **precision
  1.000, recall 1.000** (zero false positives) **on that 36-passage set**. It handles
  absolute citations, enumerated `§§` lists (guarding the trap where a list runs into a new
  citation), and the qualified prose form (`section 1983 of title 42, United States Code`)
  which fires only when the code name is present; it also caught and fixed a free-text
  section-truncation bug. **That gold-set precision did not generalise**: running the same
  detector over every federal body
  ([`reports/M2_in_body_detection.md`](reports/M2_in_body_detection.md)) found two defect
  classes the 36 passages did not cover — list members folding their subsection into the
  section, and a greedy title absorbing adjacent digits from flattened tables and dropped
  line-leading characters. Both are fixed (`title_in_range` is enforced as a
  `ParsedCitation` model invariant, not only a parser rule) and the corpus scan carries a
  zero-valued regression guard, but the title check only catches *impossible* titles —
  in-range corruption remains undetected.

## Setup

The dataset is **gated** on Hugging Face. A human must accept the dataset terms
and provide a read token:

```bash
export HF_TOKEN=hf_...   # a token with gated-repo read access
```

Install deps and download the M0 sample (verified against `SHA256SUMS.json`):

```bash
uv sync
uv run python scripts/download.py            # M0 sample → data/v2026.08/
```

The installed command exposes the maintained audit entry points:

```bash
uv run open-us-law-citation --help
uv run open-us-law-citation ca-probe --help
uv run open-us-law-citation identity-manifest --help
uv run open-us-law-citation coverage-baseline --help
```

The project was renamed from `open-us-law-coverage`. The distribution is now
`open-us-law-citation` and the import package is `open_us_law_citation`; the old
`open-us-law-coverage` **command** is kept as a compatibility alias, but the old
*import* name is gone, so `import open_us_law_coverage` must be updated to
`import open_us_law_citation`.

The project is licensed under Apache-2.0. Legal text in the upstream dataset is
public-domain government material; the dataset's compilation has its own CC BY 4.0
terms.

## Reproduce the M0 report

```bash
uv run python -m open_us_law_citation.recon \
  data/v2026.08/*.parquet --snapshot v2026.08 --out reports/M0_recon.md
```

The recon harness accepts any file glob, so it can be pointed at the full
229-file snapshot once downloaded.

## Layout

- `src/open_us_law_citation/recon.py` — M0 reconnaissance harness.
- `src/open_us_law_citation/identity_collisions.py` — M0.5A `act_id`-collision
  analysis (DuckDB, spills to disk so the 11 GB federal `text` column is safe).
- `src/open_us_law_citation/segment_provenance.py` — M0.5A.1 collision-provenance
  + segment-order spike (DuckDB `file_row_number`).
- `src/open_us_law_citation/source_record.py` — M1A immutable
  `CanonicalSourceRecord` core (lossless serializer + boundary-enforcing model).
- `src/open_us_law_citation/derived/` — M1A.5 shared derived-artifact foundation
  (provenance DAG + `payload_hash`; identity group/member, classification, quality,
  assembly contracts; and the concrete identity-strategy producers in
  `identity_strategies.py`).
- `src/open_us_law_citation/identity_manifest.py` — M1A.5 C.3 deterministic
  full-snapshot identity manifest (DuckDB-streamed structural scan of every file;
  real producers over each colliding identity group).
- `src/open_us_law_citation/hierarchy.py` — M0.5B2 hierarchy stress test
  (breadcrumb → normalized `HierarchyNode[]` / `StructuralPath` + topology report).
- `src/open_us_law_citation/ca_probe.py` — M0.5B3 CA abstraction-falsification
  probe (runs the built artifact types over CA; emits the interface-change list).
- `src/open_us_law_citation/coverage_baseline.py` — COV-1A official-inventory
  projection, provision crosswalk, discrepancy manifest, and scorecard renderer.
- `src/open_us_law_citation/citation_parser.py` — M2 federal exact-citation grammar
  (USC/CFR → `ParsedCitation` / `ReferenceMention`) + parse self-check + Stage-A detection.
- `src/open_us_law_citation/in_body_detection.py` — M2 corpus-scale in-body detection
  (DuckDB-streamed run of the detector over the whole `text` column + cross-ref agreement
  + an impossible-title precision tripwire).
- `src/open_us_law_citation/cfr_assembly.py` — CFR-A1 commissioning frame
  (classifies every multi-row `CFR_*` group from the snapshot alone; emits no assembly).
- `src/open_us_law_citation/text_integrity.py` — snapshot text-integrity audit
  (truncated bodies, captured UI chrome, impossible-title citations; needs no oracle).
- `tests/` — golden-fixture acceptance suite (`uv run pytest`).
- `scripts/download.py` — gated download + SHA-256 verification.
- `PRIORITIES.md` — authoritative product priorities and their measurement rules.
- `oracles/` — machine-validated corpus currency and oracle-edition registry.
- `reports/` — generated reports (committed).
- `data/` — downloaded snapshots (gitignored; reproduce via `scripts/download.py`).
