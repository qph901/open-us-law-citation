"""Hermetic tests for the snapshot text-integrity audit.

The detectors must count only *provable* damage. The trap they were written against: an
earlier line-start detector matched any citation that happened to begin a line, reporting
77,664 defects in the regulations corpus where the real figure is 505.
"""

from __future__ import annotations

import pyarrow as pa
import pyarrow.parquet as pq

from open_us_law_citation.text_integrity import render_report, scan_file


def _write(path, texts, xrefs=None):
    n = len(texts)
    pq.write_table(
        pa.table({
            "act_id": pa.array([f"CFR_T1_P1_S1_{i}" for i in range(n)], pa.string()),
            "text": pa.array(texts, pa.string()),
            "cross_references_usc": pa.array(xrefs or ["[]"] * n, pa.string()),
        }),
        path,
    )


def test_truncated_head_counts_midword_starts_only(tmp_path):
    path = tmp_path / "a.parquet"
    _write(path, [
        "ited States or any State or any subdivision thereof.",  # truncated mid-word
        "The Commission shall issue findings.",                  # clean
        "(a) Definitions apply to this part.",                   # clean, starts with paren
        None,                                                    # null body
    ])
    st = scan_file(path)
    assert st.rows == 4 and st.non_null_text == 3
    assert st.truncated_head == 1
    assert st.truncated_examples[0][1].startswith("ited States")


def test_only_an_impossible_title_counts_and_both_damage_shapes_are_caught(tmp_path):
    """Two guards at once. `\\n42 U.S.C. 1983` is ordinary text and must not count. And the
    damage appears in OPPOSITE orders -- the lost leading digit puts the newline BEFORE the
    digits (`\\n0 CFR`), the flattened table column puts it AFTER (`2023\\nCFR`) -- so the
    detector cannot be anchored to a newline position."""
    path = tmp_path / "b.parquet"
    _write(path, [
        "See the authority at\n42 U.S.C. 1983 for details.",      # normal, NOT damage
        "Corrective Measures Implementation\n0 CFR 264.100 or",    # leading zero: damage
        "existing on January 3, 2023\nCFR 2.2. (5) Note:",         # 4 digits: damage
        "governed by\n5 U.S.C. 552 and\n50 CFR 17.11 here.",       # both valid titles
    ])
    st = scan_file(path)
    assert st.impossible_title_cites == 2


def test_ui_chrome_in_the_body_is_counted(tmp_path):
    path = tmp_path / "c.parquet"
    _write(path, [
        "Link to an amendment published at 90 FR 1. (a) The rule applies.",
        "(a) The rule applies with no banner.",
    ])
    st = scan_file(path)
    assert st.ui_chrome == 1
    assert st.chrome_examples[0][1].startswith("Link to an amendment")


def test_impossible_cross_reference_titles_include_the_55_to_59_band(tmp_path):
    """USC has 54 titles. An earlier pattern skipped 55-59, so `56:1` read as valid."""
    path = tmp_path / "d.parquet"
    _write(
        path,
        ["body"] * 5,
        xrefs=['["42:1983"]',      # valid
               '["73:499"]',       # invalid: the Gardner v. Barney U.S. Reports case
               '["56:1"]',         # invalid, and inside the band the old pattern missed
               '["54:100101"]',    # valid: 54 is the highest real title
               "[]"],
    )
    st = scan_file(path)
    assert st.corrupt_xref_titles == 2


def test_report_is_byte_stable_and_states_the_lower_bound(tmp_path):
    path = tmp_path / "e.parquet"
    _write(path, ["ited States or any State.", "Clean body here."])
    st = scan_file(path)
    r1 = render_report([st], "v2026.08")
    assert render_report([st], "v2026.08") == r1
    assert "lower bound on truncation" in r1
    assert "not a chartered milestone" in r1
