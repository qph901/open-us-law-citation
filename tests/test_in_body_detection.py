"""Hermetic tests for corpus-scale in-body detection (M2).

A tiny synthetic Parquet (the five columns the scanner reads) exercises the row-group scan,
the coarse code-token pre-filter, and the agreement algebra against ``cross_references_*`` —
including the load-bearing distinction that a **bare** in-body reference (no code token) is
skipped by the filter and lands in ``dataset-only``, never as a detection.
"""

from __future__ import annotations

import pyarrow as pa
import pyarrow.parquet as pq

from open_us_law_citation.in_body_detection import (
    _parse_xref_cfr,
    _parse_xref_usc,
    render_report,
    scan_file,
)


def _write_fixture(path):
    table = pa.table(
        {
            "text": pa.array(
                [
                    "The claim under 42 U.S.C. § 1983 stands.",   # explicit USC, in cross-refs
                    "See 5 U.S.C. § 552 for records.",            # explicit USC, NOT in cross-refs
                    "the preceding section governs here.",        # bare ref: no code token
                    "Regulated by 17 C.F.R. § 240.10b-5 today.",  # explicit CFR (same title)
                    None,                                         # null body: skipped
                ],
                pa.string(),
            ),
            "act_id": pa.array(
                ["USC_T1_S1", "USC_T1_S2", "USC_T1_S3", "CFR_T17_P240_S240_10b_5", "USC_T1_S5"],
                pa.string(),
            ),
            "title_number": pa.array([1, 1, 1, 17, 1], pa.int64()),
            "cross_references_usc": pa.array(
                ['["42:1983"]', "[]", '["10:113"]', "[]", "[]"], pa.string()
            ),
            "cross_references_cfr": pa.array(
                ["[]", "[]", "[]", '["240.10b-5"]', "[]"], pa.string()
            ),
        }
    )
    pq.write_table(table, path)


def test_xref_parsers():
    assert _parse_xref_usc('["10:113", "37:404"]') == {("10", "113"), ("37", "404")}
    assert _parse_xref_usc("[]") == set() and _parse_xref_usc(None) == set()
    # bare CFR entries take the citing row's title implicitly; a trailing dot is trimmed
    assert _parse_xref_cfr('["4.1045", "210.1."]', 43) == {("43", "4.1045"), ("43", "210.1")}
    # an explicit title:section entry wins
    assert _parse_xref_cfr('["12:226.1"]', 43) == {("12", "226.1")}
    # a part-level dict is NOT a section edge — excluded from the section comparison
    assert _parse_xref_cfr('[{"title": 40, "part": "52"}]', 43) == set()
    assert _parse_xref_cfr('[{"title": 40, "section": "52.21"}]', 43) == {("40", "52.21")}


def test_scan_counts_and_agreement(tmp_path):
    fixture = tmp_path / "fx.parquet"
    _write_fixture(fixture)
    st = scan_file(fixture)

    assert st.rows_total == 5
    assert st.rows_candidate == 3          # the two USC bodies + one CFR body carry a code token
    assert st.rows_with_detection == 3
    assert st.usc_mentions == 2 and st.cfr_mentions == 1

    # USC: (42,1983) in both; (5,552) detector-only; (10,113) is a bare ref -> dataset-only.
    assert (st.usc_both, st.usc_detector_only, st.usc_dataset_only) == (1, 1, 1)
    # CFR: the explicit 17 CFR 240.10b-5 matches the bare cross-ref under the row's title 17.
    assert (st.cfr_both, st.cfr_detector_only, st.cfr_dataset_only) == (1, 0, 0)
    assert ("usc", "5", "552") in st.usc_detector_only_ex


def test_bare_reference_is_not_a_candidate(tmp_path):
    """A body with only a bare/relative reference (no code token) is filtered out before any
    detection — it is M4's LOCAL/RELATIVE population, not an explicit-citation miss."""
    fixture = tmp_path / "fx.parquet"
    _write_fixture(fixture)
    st = scan_file(fixture)
    # row 2 ("the preceding section ...") has a dataset cross-ref but is never a candidate.
    assert st.usc_dataset_only == 1
    assert st.rows_candidate == 3  # excludes the bare-ref row and the null-text row


def test_report_is_stable(tmp_path):
    fixture = tmp_path / "fx.parquet"
    _write_fixture(fixture)
    st = scan_file(fixture)
    r1 = render_report([st], "v2026.08")
    r2 = render_report([st], "v2026.08")
    assert r1 == r2
    assert "M2/M4 boundary" in r1


def test_impossible_title_is_never_detected_and_the_tripwire_reads_zero(tmp_path):
    """The grammar refuses titles outside a code's range, so the tripwire is a regression
    guard that must read zero — `Pub. L. 95-147 U.S.C. 19` parsed title 147 before the fix."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    path = tmp_path / "oor.parquet"
    pq.write_table(
        pa.table(
            {
                "text": pa.array(
                    ["Authority: Pub. L. 95-147 U.S.C. 19.", "Valid: 42 U.S.C. § 1983."],
                    pa.string(),
                ),
                "act_id": pa.array(["USC_T1_S1", "USC_T1_S2"], pa.string()),
                "title_number": pa.array([1, 1], pa.int64()),
                "cross_references_usc": pa.array(["[]", "[]"], pa.string()),
                "cross_references_cfr": pa.array(["[]", "[]"], pa.string()),
            }
        ),
        path,
    )
    st = scan_file(path)
    assert st.usc_out_of_range == 0 and st.cfr_out_of_range == 0
    assert st.out_of_range_ex == set()
    # Both rows carry a code token, but only the valid citation yields a detection.
    assert st.rows_candidate == 2 and st.rows_with_detection == 1
    assert st.usc_detector_only_ex == {("usc", "42", "1983")}
    assert "Precision limits found at corpus scale" in render_report([st], "v2026.08")
