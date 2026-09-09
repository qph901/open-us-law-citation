"""Hermetic tests for the CFR-A1 commissioning frame.

The classifier's job is to separate three physically different things that all look like
"one act_id, several rows": byte-identical duplicates, overlapping variant captures, and
genuinely disjoint segments. Getting the middle one wrong is the hard failure CFR-A1 has
zero tolerance for -- concatenating a variant pair emits operative text twice under a
whole-section citation.
"""

from __future__ import annotations

import pyarrow as pa
import pyarrow.parquet as pq

from open_us_law_citation.cfr_assembly import (
    GroupRelation,
    MemberRow,
    analyze_group,
    build_frame,
    render_report,
)


def _row(frn: int, text: str) -> MemberRow:
    return MemberRow(frn=frn, text_sha256=f"sha256:{hash(text) & 0xFFFF:04x}",
                     length=len(text), text=text)


def _identical(frn: int, text: str) -> MemberRow:
    return MemberRow(frn=frn, text_sha256="sha256:same", length=len(text), text=text)


def test_byte_identical_group_needs_no_composition():
    body = "(a) The operator shall maintain records."
    g = analyze_group("CFR_T10_P1_S1_1", [_identical(1, body), _identical(9, body)])
    assert g.relation == GroupRelation.DUPLICATE_ONLY
    assert g.composable_without_an_oracle is True


def test_containment_is_a_variant_capture_not_a_segment():
    """The real shape in v2026.08: one row carries an eCFR amendment banner, the other
    does not, and the shorter sits wholly inside the longer. Concatenating duplicates."""
    core = "(a) No person may transfer special nuclear material contrary to the interest."
    g = analyze_group("CFR_T10_P171_S171_15",
                      [_row(1, core), _row(2, "Link to an amendment published. " + core)])
    assert g.relation == GroupRelation.VARIANT_CAPTURE
    assert g.contained_pairs == 1
    assert g.composable_without_an_oracle is False


def test_shared_suffix_reads_as_variant_only_above_the_threshold():
    """Both sides of the 0.50 cut, which sits in an empty valley of the real distribution
    (38.3% of non-duplicate groups below 0.01, 42.7% at or above 0.90).

    Below it the classifier must NOT force a bucket: it abstains, which is the safe
    outcome, because an unrecognised variant pair is the one that gets concatenated.
    """
    tail = "the same closing sentence of the section."
    strong = analyze_group("CFR_T1_P1_S1_1",
                           [_row(1, "X" * 20 + tail), _row(2, "Y" * 10 + tail)])
    assert strong.max_overlap_ratio >= 0.5
    assert strong.relation == GroupRelation.VARIANT_CAPTURE

    weak = analyze_group("CFR_T1_P1_S1_2",
                         [_row(1, "X" * 100 + tail), _row(2, "Y" * 60 + tail)])
    assert weak.max_overlap_ratio < 0.5
    assert weak.relation == GroupRelation.UNDETERMINED   # abstains, never forced


def test_disjoint_rows_with_a_midthought_seam_are_the_composer_candidates():
    g = analyze_group(
        "CFR_T10_P2_S2_390",
        [_row(1, "(a) The Commission shall consider each application and"),
         _row(2, "shall issue findings within 30 days.")],
    )
    assert g.relation == GroupRelation.CANDIDATE_SEGMENTED
    assert g.continuation_seams == 1 and g.seams == 1


def test_disjoint_rows_without_a_seam_abstain():
    """Two complete, unrelated sentences: no evidence of segmentation, so abstain rather
    than guess an order."""
    g = analyze_group(
        "CFR_T10_P26_S26_205",
        [_row(1, "(a) Definitions apply to this part."),
         _row(2, "(b) Separate requirements govern reporting.")],
    )
    assert g.relation == GroupRelation.UNDETERMINED
    assert g.continuation_seams == 0


def test_overlap_is_measured_across_every_pair_not_only_adjacent_ones():
    """A 3-row group can hold a variant capture that is not physically consecutive; only
    an all-pairs comparison catches it."""
    core = "(a) The licensee shall report each incident to the Commission promptly."
    rows = [_row(1, core), _row(5, "(b) Unrelated middle provision text goes here."),
            _row(9, "Link to an amendment published. " + core)]
    g = analyze_group("CFR_T10_P2_S2_202", rows)
    assert g.contained_pairs == 1
    assert g.relation == GroupRelation.VARIANT_CAPTURE


def test_frame_over_a_fixture_counts_only_multi_row_cfr_groups(tmp_path):
    path = tmp_path / "reg.parquet"
    body = "(a) Identical duplicated row."
    pq.write_table(
        pa.table({
            "act_id": pa.array(
                ["CFR_T1_P1_S1_1", "CFR_T1_P1_S1_1",   # multi-row group
                 "CFR_T1_P1_S1_2",                      # single row: not a group
                 "FR_PRORULE_1", "FR_PRORULE_1"],       # FR: out of scope here
                pa.string()),
            "text": pa.array([body, body, "single", "fr a", "fr b"], pa.string()),
        }),
        path,
    )
    frame = build_frame(path)
    assert frame.cfr_rows == 3 and frame.cfr_act_ids == 2
    assert [g.act_id for g in frame.groups] == ["CFR_T1_P1_S1_1"]
    assert frame.groups[0].relation == GroupRelation.DUPLICATE_ONLY
    assert frame.multi_row_rows == 2

    report = render_report(frame, "v2026.08")
    assert render_report(frame, "v2026.08") == report          # byte-stable
    assert "CFR-A2 stays gated" in report
    assert "Concatenation is the wrong primitive" in report
