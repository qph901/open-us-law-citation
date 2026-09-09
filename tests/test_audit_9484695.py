"""Regressions for the twelve defects found in the audit of commit 9484695.

Kept as one file so the audited behaviours stay pinned together; each test names the
finding it locks down.
"""

from __future__ import annotations

import pytest

import scripts.stage_oracle as st
from open_us_law_citation.cfr_assembly import GroupRelation, MemberRow, analyze_group
from open_us_law_citation.citation_parser import (
    build_reference_mention,
    detect_mentions,
    parse_citation,
)
from open_us_law_citation.coverage_baseline import (
    DatasetCandidate,
    DatasetEvidence,
    FederalCorpus,
    OfficialInventory,
    OfficialProvision,
    ProvisionKey,
    TitleCurrency,
    build_baseline,
    coverage_counts,
    coverage_rates,
    text_fingerprints,
)
from open_us_law_citation.derived.provenance import check_payload_collisions
from open_us_law_citation.oracle_manifest import CutoffStatus, OracleKind


# --- P1 #1 ------------------------------------------------------------------
def test_list_does_not_consume_the_prefix_of_a_new_two_digit_title():
    """The list guard rejected `12` because a code follows, then the section backtracked
    to `1` (whose lookahead passes, since `2` follows), emitting a phantom title-42
    section 1 whose span suppressed the real `12 U.S.C. § 34` as an overlap."""
    got = [(m.parsed.parsed_title, m.parsed.parsed_section)
           for m in detect_mentions("42 U.S.C. §§ 1983 and 12 U.S.C. § 34")]
    assert got == [("42", "1983"), ("12", "34")]


@pytest.mark.parametrize("title", ["5", "12", "42"])
def test_list_guard_holds_for_every_title_width(title):
    got = [(m.parsed.parsed_title, m.parsed.parsed_section)
           for m in detect_mentions(f"42 U.S.C. §§ 1983 and {title} U.S.C. § 34")]
    assert got == [("42", "1983"), (title, "34")]


# --- P1 #2 ------------------------------------------------------------------
def test_hyphenated_usc_section_is_not_truncated_to_a_different_provision():
    """`2000e-2` is Title VII's employment-discrimination section; `2000e` is definitions.
    Emitting the prefix at confidence 1.0 was a silent wrong answer."""
    (mention,) = detect_mentions("42 U.S.C. § 2000e-2(a)")
    assert mention.parsed.parsed_section == "2000e-2"
    assert mention.parsed.parsed_subsection == "(a)"


def test_a_usc_section_range_abstains_rather_than_truncating():
    """`668dd-668ee` is a RANGE. Sampled real bodies show every hyphenated USC identifier
    has a letter before the hyphen and a numeric tail; a range is not that shape, and
    abstaining beats emitting `668dd`."""
    assert detect_mentions("16 U.S.C. § 668dd-668ee") == []


def test_the_dataset_underscore_rendering_still_parses():
    assert parse_citation("10 U.S.C. § 222e_2").parsed_section == "222e_2"


# --- P2 #3 / #4 -------------------------------------------------------------
def test_ordinary_cfr_subsection_is_separate_from_the_section():
    """Of 168,488 real CFR section numbers, 1,455 have INTERIOR parens and only 8 trail.
    A trailing group is an ordinary paragraph pointer, not part of the identity."""
    (mention,) = detect_mentions("5 CFR 330.601(a)(1)")
    assert mention.parsed.parsed_section == "330.601"
    assert mention.parsed.parsed_subsection == "(a)(1)"


@pytest.mark.parametrize(
    "text,section",
    [
        ("26 CFR 41.6151(a)-1", "41.6151(a)-1"),          # interior parens: identity
        ("26 CFR 275.202(a)(11)(G)-1", "275.202(a)(11)(G)-1"),
        ("17 CFR 240.11a1-4(T)", "240.11a1-4(T)"),        # the temporary marker
    ],
)
def test_identifier_internal_parentheses_are_kept(text, section):
    assert detect_mentions(text)[0].parsed.parsed_section == section


def test_a_prose_closing_parenthesis_is_not_part_of_the_section():
    """The old character class accepted a lone `)`, so a parenthesised citation produced
    section `240.10b-5)` — a key that matches nothing."""
    (mention,) = detect_mentions("See (17 CFR 240.10b-5).")
    assert mention.parsed.parsed_section == "240.10b-5"
    assert ")" not in mention.raw_reference_text


# --- P2 #5 ------------------------------------------------------------------
def test_staging_refuses_a_well_formed_xml_error_body():
    """`<error>…</error>` parses and is not HTML, so well-formedness alone would certify
    an API failure as a title — the title then vanishes from the denominator while the run
    reports success."""
    with pytest.raises(ValueError, match="refusing to stage"):
        st._require_valid_xml(
            "title-2.xml", b"<error>Temporarily unavailable</error>", expected_root="ECFR"
        )
    st._require_valid_xml("title-2.xml", b"<ECFR><DIV1/></ECFR>", expected_root="ECFR")


# --- P2 #7 ------------------------------------------------------------------
def test_reserved_entries_do_not_inflate_currency_rates():
    """Reserved leaves `expected`, so it must leave every rate's numerator too — otherwise
    stale_percent exceeded 100%."""
    inventory = OfficialInventory(
        corpus=FederalCorpus.CFR, oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR, edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml", source_sha256="a" * 64,
        title_currency=(TitleCurrency("1", "2026-08-26", "fixture"),),
        provisions=(
            OfficialProvision.from_text(
                key=ProvisionKey(FederalCorpus.CFR, "1", "1.1"), official_id="o1",
                source_url="https://official.example/a", text="Live."),
            OfficialProvision.from_text(
                key=ProvisionKey(FederalCorpus.CFR, "1", "1.2"), official_id="o2",
                source_url="https://official.example/b", text="[Reserved]", reserved=True),
        ),
    )

    def candidate(section: str, ordinal: int) -> DatasetCandidate:
        raw, norm = text_fingerprints("stale text")
        return DatasetCandidate(
            key=ProvisionKey(FederalCorpus.CFR, "1", section),
            source_record_id=f"srr:{ordinal}", act_id=f"CFR_T1_S{ordinal}",
            source_url=None, raw_text_sha256=raw, normalized_text_sha256=norm)

    baseline = build_baseline(
        inventory=inventory, inventory_sha256="b" * 64,
        dataset=DatasetEvidence(
            snapshot="v-test", dataset_revision="rev", source_file="f.parquet",
            source_file_sha256="c" * 64, legal_content_cutoff="2020-01-01",
            cutoff_status=CutoffStatus.ESTABLISHED),
        candidates=[candidate("1.1", 1), candidate("1.2", 2)],
    )
    counts = coverage_counts(baseline.entries)
    assert counts["expected"] == 1 and counts["reserved"] == 1
    assert counts["stale"] <= counts["expected"]
    assert float(coverage_rates(counts)["stale_percent"]) <= 100.0


# --- P2 #8 ------------------------------------------------------------------
def test_a_null_text_group_member_forces_abstention():
    """Dropping the null member left a one-row remnant classified `duplicate_only` —
    missing evidence turned into apparent agreement."""
    rows = [MemberRow(frn=1, text_sha256="sha256:a", length=4, text="Body"),
            MemberRow(frn=2, text_sha256=None, length=None, text=None)]
    group = analyze_group("CFR_T1_S1", rows)
    assert group.size == 2
    assert group.relation == GroupRelation.UNDETERMINED
    assert group.composable_without_an_oracle is False


# --- P2 #9 ------------------------------------------------------------------
@pytest.mark.parametrize("gap", [" ", "\n", "  ", "\t"])
def test_scan_prefilter_is_a_superset_of_the_detector(gap):
    """The SQL prefilter used literal spaces in the spelled-out code names while the
    detector accepts `\\s+`, so an ordinary line wrap hid a real citation from the scan."""
    import re

    from open_us_law_citation.in_body_detection import _CANDIDATE_RE

    body = f"section 1983 of title 42, United{gap}States Code applies."
    assert detect_mentions(body), "detector should find it"
    assert re.search(_CANDIDATE_RE, body), "prefilter must not exclude it"


# --- P2 #10 -----------------------------------------------------------------
def test_mention_context_participates_in_the_derivation_address():
    """`structural_path` lands in the payload, so leaving it out of `config_hash` gave two
    different payloads one artifact_id — which the collision tripwire then flagged."""
    (parsed,) = [m.parsed for m in detect_mentions("42 U.S.C. § 1983")]
    a = build_reference_mention(parsed, "42 U.S.C. § 1983", 0, 16,
                                source_record_id="srr:1", structural_path="/t42/c21/s1983")
    b = build_reference_mention(parsed, "42 U.S.C. § 1983", 0, 16,
                                source_record_id="srr:1", structural_path="/t42/c21/s1983/a")
    assert a.provenance.artifact_id != b.provenance.artifact_id
    check_payload_collisions([a, b])   # takes the artifacts, not their provenance


# --- P2 #11 -----------------------------------------------------------------
def test_snapshot_diff_refuses_a_corpus_whose_act_id_repeats():
    """Both hash dicts kept only the last row per id, so physical row ORDER decided
    whether a provision counted as amended. Regulations repeat act_id by design."""
    import polars as pl

    from open_us_law_citation.snapshot_diff import _require_unique_act_ids

    frame = pl.DataFrame({"act_id": ["CFR_T1_S1", "CFR_T1_S1"], "text": ["Alpha", "Beta"]})
    with pytest.raises(ValueError, match="repeats act_id"):
        _require_unique_act_ids(frame, "new")
