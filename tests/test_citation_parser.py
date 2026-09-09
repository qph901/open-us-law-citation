"""Hermetic acceptance suite for the M2 citation parser.

No staged bytes or network: grammar tests use literal strings, and the self-check test
synthesizes a tiny Parquet fixture. Asserts the project invariants — abstain rather than
guess, provenance on the interpretation boundary, and the D2 collision tripwire covers a
mention.
"""

from __future__ import annotations

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from open_us_law_coverage.citation_parser import (
    DETECTION_GOLD,
    _DETECTION_MIN_PRECISION,
    _DETECTION_MIN_RECALL,
    ParsedCitation,
    ReferenceType,
    analyze_file,
    build_reference_mention,
    detect_mentions,
    detection_metrics,
    parse_cfr_citation,
    parse_citation,
    parse_usc_citation,
    render_detection_report,
    render_report,
)
from open_us_law_coverage.coverage_baseline import FederalCorpus
from open_us_law_coverage.derived import ArtifactType, check_payload_collisions


# --- USC grammar ----------------------------------------------------------------


@pytest.mark.parametrize(
    "text,title,section",
    [
        ("42 U.S.C. § 1983", "42", "1983"),
        ("10 U.S.C. § 9775 (2024)", "10", "9775"),
        ("42 USC 1983", "42", "1983"),
        ("42 U.S.C. 1983", "42", "1983"),
        ("42 U.S.C.A. § 1983", "42", "1983"),
        ("43 U.S.C. § 1613a", "43", "1613a"),
        ("15 U.S.C. § 77aa", "15", "77aa"),        # multi-letter suffix
        ("12 U.S.C. § 1749aaa", "12", "1749aaa"),  # triple-letter suffix
        ("10 U.S.C. § 222e_2", "10", "222e_2"),    # underscore tail
        ("  42 U.S.C. § 1983  ", "42", "1983"),
    ],
)
def test_parse_usc_absolute(text, title, section):
    p = parse_usc_citation(text)
    assert p is not None
    assert p.parsed_corpus == FederalCorpus.USC
    assert (p.parsed_title, p.parsed_section) == (title, section)
    assert p.reference_type == ReferenceType.ABSOLUTE
    assert p.parser_method == "usc_grammar_v1"
    assert p.parser_confidence == 1.0
    assert p.parsed_part is None


def test_parse_usc_subsection():
    p = parse_usc_citation("42 U.S.C. § 1983(a)(2)")
    assert p is not None
    assert (p.parsed_title, p.parsed_section, p.parsed_subsection) == ("42", "1983", "(a)(2)")


def test_parse_usc_qualified():
    p = parse_usc_citation("section 1983 of title 42")
    assert p is not None
    assert (p.parsed_title, p.parsed_section) == ("42", "1983")
    assert p.reference_type == ReferenceType.QUALIFIED
    assert p.parser_confidence == 0.9
    assert parse_usc_citation("Section 1983 of Title 42, United States Code") is not None


# --- CFR grammar ----------------------------------------------------------------


@pytest.mark.parametrize(
    "text,title,part,section",
    [
        ("17 CFR 240.10b-5", "17", "240", "240.10b-5"),
        ("5 C.F.R. § 330.601 (2026)", "5", "330", "330.601"),
        ("43 C.F.R. § 1864.0-3", "43", "1864", "1864.0-3"),
        ("42 C.F.R. § 423.1002", "42", "423", "423.1002"),
        ("12 C.F.R. § 261a.1", "12", "261a", "261a.1"),          # letter-suffixed part
        ("41 C.F.R. § 101-6.2104", "41", "101-6", "101-6.2104"),  # hyphenated part (FPMR)
        ("41 C.F.R. § 101-6.205-2", "41", "101-6", "101-6.205-2"),
        # v2: embedded subsection + trailing (T) are part of the CFR section identity
        ("26 C.F.R. § 41.6151(a)-1", "26", "41", "41.6151(a)-1"),
        ("26 C.F.R. § 31.3401(a)(8)(B)-1", "26", "31", "31.3401(a)(8)(B)-1"),
        ("17 C.F.R. § 240.11a1-4(T)", "17", "240", "240.11a1-4(T)"),
        ("5 C.F.R. § 330.601 (2026)", "5", "330", "330.601"),     # year still not captured
    ],
)
def test_parse_cfr_absolute(text, title, part, section):
    p = parse_cfr_citation(text)
    assert p is not None
    assert p.parsed_corpus == FederalCorpus.CFR
    assert (p.parsed_title, p.parsed_part, p.parsed_section) == (title, part, section)
    assert p.parser_method == "cfr_grammar_v3"


@pytest.mark.parametrize(
    "text,title,section",
    [
        ("14 C.F.R. § 1-1", "14", "1-1"),
        ("14 C.F.R. § 03", "14", "03"),
        ("14 C.F.R. § 19-4", "14", "19-4"),
        ("14 C.F.R. § 9", "14", "9"),
    ],
)
def test_parse_cfr_dotless_part241(text, title, section):
    """14 CFR Part 241 sections have no part.section dot; the part is not in the citation,
    so it parses with parsed_part=None at reduced confidence rather than being fabricated."""
    p = parse_cfr_citation(text)
    assert p is not None
    assert p.parsed_corpus == FederalCorpus.CFR
    assert (p.parsed_title, p.parsed_section, p.parsed_part) == (title, section, None)
    assert p.parser_confidence == 0.75
    assert p.parser_method == "cfr_grammar_v3"


def test_cfr_dotted_still_beats_dotless():
    """A normal dotted section keeps its part and full confidence (dotless is a fallback)."""
    p = parse_cfr_citation("5 C.F.R. § 330.601")
    assert p.parsed_part == "330" and p.parser_confidence == 1.0


def test_cfr_v2_keeps_year_separate_from_embedded_subsection():
    """A trailing (YYYY) is space-separated and never swallowed, even though an embedded
    (a) with no leading space IS part of the section identity."""
    p = parse_cfr_citation("26 C.F.R. § 41.6151(a)-1 (2024)")
    assert p is not None and p.parsed_section == "41.6151(a)-1"


def test_parse_cfr_qualified():
    p = parse_cfr_citation("section 240.10b-5 of title 17")
    assert p is not None
    assert (p.parsed_title, p.parsed_part, p.parsed_section) == ("17", "240", "240.10b-5")
    assert p.reference_type == ReferenceType.QUALIFIED


def test_dispatcher_routes_by_code():
    assert parse_citation("17 CFR 240.10b-5").parsed_corpus == FederalCorpus.CFR
    assert parse_citation("42 U.S.C. § 1983").parsed_corpus == FederalCorpus.USC


# --- Abstention (never guess) ---------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "",
        "hello world",
        "see the statute",
        "42 U.S.C.",            # no section
        "title 42 generally",
        "Public Law 118-274",
        "89 Fed. Reg. 12345",   # Federal Register, not USC/CFR
    ],
)
def test_abstains_on_non_citations(text):
    assert parse_citation(text) is None


# --- ParsedCitation validation --------------------------------------------------


def test_parsed_citation_rejects_bad_shape():
    with pytest.raises(ValueError):  # a USC citation never carries a part
        ParsedCitation(
            FederalCorpus.USC, "42", "1983", ReferenceType.ABSOLUTE, "m", 1.0, parsed_part="21"
        )
    with pytest.raises(ValueError):  # relative types are not emitted by M2
        ParsedCitation(FederalCorpus.USC, "42", "1983", ReferenceType.LOCAL, "m", 1.0)
    with pytest.raises(ValueError):  # confidence out of range
        ParsedCitation(FederalCorpus.USC, "42", "1983", ReferenceType.ABSOLUTE, "m", 1.5)


def test_cfr_partless_is_now_allowed():
    """A dotless CFR citation legitimately has no part (14 CFR Part 241)."""
    p = ParsedCitation(FederalCorpus.CFR, "14", "1-1", ReferenceType.ABSOLUTE, "m", 0.75)
    assert p.parsed_part is None


# --- ReferenceMention + provenance ----------------------------------------------


def test_reference_mention_provenance_and_payload():
    p = parse_usc_citation("42 U.S.C. § 1983")
    m = build_reference_mention(p, "42 U.S.C. § 1983", 0, 16, source_record_id="rec-1")
    assert m.provenance.artifact_type == ArtifactType.REFERENCE_MENTION
    assert m.provenance.source_record_ids() == ("rec-1",)
    assert m.payload_hash.startswith("pay:sha256:")
    # Standalone (query) mention: no source-record edge.
    q = build_reference_mention(p, "42 U.S.C. § 1983", 0, 16)
    assert q.provenance.source_record_ids() == ()


def test_two_mentions_in_one_record_do_not_collide():
    """Distinct citations in the same source record get distinct artifact_ids and pass
    the D2 payload-collision tripwire."""
    a = build_reference_mention(
        parse_usc_citation("42 U.S.C. § 1983"), "42 U.S.C. § 1983", 0, 16, source_record_id="r"
    )
    b = build_reference_mention(
        parse_usc_citation("42 U.S.C. § 1985"), "42 U.S.C. § 1985", 20, 36, source_record_id="r"
    )
    assert a.provenance.artifact_id != b.provenance.artifact_id
    check_payload_collisions([a, b])  # must not raise


def test_reference_mention_rejects_edge_mismatch():
    p = parse_usc_citation("42 U.S.C. § 1983")
    m = build_reference_mention(p, "42 U.S.C. § 1983", 0, 16, source_record_id="rec-1")
    with pytest.raises(ValueError):  # payload disagrees with a hand-set stale hash
        type(m)(
            parsed=m.parsed,
            raw_reference_text=m.raw_reference_text,
            start_char=m.start_char,
            end_char=m.end_char,
            provenance=m.provenance,
            payload_hash="pay:sha256:" + "0" * 64,
            source_record_id="rec-1",
        )


# --- Detection scan -------------------------------------------------------------


def test_detect_mentions_finds_usc_and_cfr_sorted():
    text = "See 42 U.S.C. § 1983 and also 17 CFR 240.10b-5 for details."
    ms = detect_mentions(text, source_record_id="r9")
    assert [m.parsed.parsed_corpus for m in ms] == [FederalCorpus.USC, FederalCorpus.CFR]
    assert ms[0].start_char < ms[1].start_char
    # spans point at the actual citation text
    assert text[ms[0].start_char:ms[0].end_char].startswith("42 U.S.C")
    assert all(m.provenance.source_record_ids() == ("r9",) for m in ms)


def test_detect_no_double_count_cfr_as_usc():
    ms = detect_mentions("5 C.F.R. § 330.601")
    assert len(ms) == 1
    assert ms[0].parsed.parsed_corpus == FederalCorpus.CFR


@pytest.mark.parametrize(
    "text,section",
    [
        ("See 17 CFR 240.10b-5 for the rule.", "240.10b-5"),
        ("Under 5 C.F.R. § 330.601 today.", "330.601"),
        ("At 43 C.F.R. § 1864.0-3 and more.", "1864.0-3"),
        ("Per 26 C.F.R. § 41.6151(a)-1 here.", "41.6151(a)-1"),
    ],
)
def test_detect_does_not_truncate_cfr_section_in_free_text(text, section):
    """Regression: in free-text scanning the CFR section was truncated (240.10b-5 -> 240.1)
    because the alternation preferred the single-char branch; the greedy form fixes it."""
    ms = detect_mentions(text)
    assert len(ms) == 1
    assert ms[0].parsed.parsed_section == section


# --- Stage-A detection metrics (hand-labelled gold) -----------------------------


def test_detection_meets_recorded_baseline():
    metrics, fps, fns = detection_metrics()
    # Precision is the hard, per-corpus requirement (precision-first design).
    for key in ("USC", "CFR", "all"):
        assert metrics[key].precision >= _DETECTION_MIN_PRECISION, (key, metrics[key].precision)
    # Recall is measured overall; the one documented gap is an enumerated `§§` list member.
    assert metrics["all"].recall >= _DETECTION_MIN_RECALL, metrics["all"].recall
    assert fps == []  # never fire on a distractor


def test_detection_no_false_positive_on_any_distractor():
    for text, expected in DETECTION_GOLD:
        if not expected:  # pure-distractor passage
            assert detect_mentions(text) == [], text


def test_detect_enumerated_section_list():
    ms = detect_mentions("Brought under 42 U.S.C. §§ 1983, 1985 jointly.")
    got = [(m.parsed.parsed_title, m.parsed.parsed_section) for m in ms]
    assert got == [("42", "1983"), ("42", "1985")]  # both members, shared title


def test_detect_three_item_and_list():
    ms = detect_mentions("It cites 42 U.S.C. §§ 1981, 1982, and 1983 together.")
    assert [m.parsed.parsed_section for m in ms] == ["1981", "1982", "1983"]


def test_detect_cfr_enumerated_list():
    ms = detect_mentions("The rules at 17 C.F.R. §§ 240.10b-5, 240.14a-9 apply.")
    got = [(m.parsed.parsed_title, m.parsed.parsed_section) for m in ms]
    assert got == [("17", "240.10b-5"), ("17", "240.14a-9")]


def test_detect_list_does_not_absorb_a_following_new_citation():
    """The precision trap: a §§ list running into a different citation must not attribute
    the new citation's number to the list's title."""
    ms = detect_mentions("Under 42 U.S.C. §§ 1983, 1985 and 5 U.S.C. § 552, relief lies.")
    got = {(m.parsed.parsed_title, m.parsed.parsed_section) for m in ms}
    assert got == {("42", "1983"), ("42", "1985"), ("5", "552")}
    assert ("42", "5") not in got  # never a phantom title-42 §5


def test_single_section_sign_does_not_start_a_list():
    """A single § followed by 'and <n> U.S.C.' is two separate citations, not a list."""
    ms = detect_mentions("See 42 U.S.C. § 1983 and 5 U.S.C. § 552.")
    got = {(m.parsed.parsed_title, m.parsed.parsed_section) for m in ms}
    assert got == {("42", "1983"), ("5", "552")}


def test_detect_qualified_prose_form():
    ms = detect_mentions("Liability under Section 1983 of Title 42, United States Code, is settled.")
    assert len(ms) == 1
    assert (ms[0].parsed.parsed_title, ms[0].parsed.parsed_section) == ("42", "1983")
    assert ms[0].parsed.reference_type == ReferenceType.QUALIFIED
    cfr = detect_mentions("The rule in section 240.10b-5 of title 17, Code of Federal Regulations.")
    assert (cfr[0].parsed.parsed_corpus, cfr[0].parsed.parsed_section) == (
        FederalCorpus.CFR, "240.10b-5")


@pytest.mark.parametrize(
    "text",
    [
        "Section 1983 of title 42 of the lease agreement governs.",  # no code name
        "Section 5 of title I of the Act controls here.",            # non-numeric title, no code
        "See section 5 of the Agreement.",                          # no 'of title N'
    ],
)
def test_detect_qualified_requires_code_name(text):
    """Precision guard: the qualified form fires ONLY with the spelled-out code name."""
    assert detect_mentions(text) == []


def test_detection_report_is_stable():
    r1 = render_detection_report()
    r2 = render_detection_report()
    assert r1 == r2
    assert "M2 citation-detector Stage-A metrics" in r1
    assert "None — the detector fired on no distractor." in r1


# --- Self-check harness (Stage-B metric on the dataset's own labels) -------------


def _write_fixture(path):
    rows = {
        "act_id": [
            "USC_T42_C21_S1983", "USC_T10_C979_S9775",
            "CFR_T5_P330_S330_601", "CFR_T17_P240_S240_10b_5",
            "CFR_T10_P1013_S1013_1",               # null title_number -> recovered
            "FR_2024_12345",                       # Federal Register: expected abstain
            "USC_T42_C21_S9999",                   # structured field disagrees -> mismatch
        ],
        "citation_short": [
            "42 U.S.C. § 1983", "10 U.S.C. § 9775",
            "5 C.F.R. § 330.601", "17 C.F.R. § 240.10b-5",
            "10 C.F.R. § 1013.1",
            "89 Fed. Reg. 12345",
            "42 U.S.C. § 1983",                    # says 1983 but section_number is 9999
        ],
        "citation": ["x"] * 7,
        "title_number": [42, 10, 5, 17, None, None, 42],
        "section_number": ["1983", "9775", "330.601", "240.10b-5", "1013.1", None, "9999"],
    }
    table = pa.table(
        {
            "act_id": pa.array(rows["act_id"], pa.string()),
            "citation_short": pa.array(rows["citation_short"], pa.string()),
            "citation": pa.array(rows["citation"], pa.string()),
            "title_number": pa.array(rows["title_number"], pa.int64()),
            "section_number": pa.array(rows["section_number"], pa.string()),
        }
    )
    pq.write_table(table, path)


def test_selfcheck_scores_and_baselines(tmp_path):
    fixture = tmp_path / "fx.parquet"
    _write_fixture(fixture)
    results = analyze_file(fixture)

    usc = results["USC"]
    assert usc.rows == 3 and usc.exact == 2 and usc.mismatch == 1 and usc.abstained == 0
    assert usc.mismatch_examples  # the T42/9999-vs-1983 row

    cfr = results["CFR"]
    assert cfr.rows == 3 and cfr.exact == 2 and cfr.mismatch == 0
    assert cfr.recovered == 1  # the null-title_number row the parser backfilled

    other = results["other"]  # the FR row: expected abstention, not scored
    assert other.rows == 1 and other.abstained == 1 and other.parsed == 0


def test_report_is_stable_under_shuffled_input(tmp_path):
    a = tmp_path / "a.parquet"
    _write_fixture(a)
    r1 = render_report([("fx", analyze_file(a))], "v2026.08")
    r2 = render_report([("fx", analyze_file(a))], "v2026.08")
    assert r1 == r2
    assert "M2 citation-parser self-check" in r1


def test_list_member_subsection_matches_the_primary_form():
    """A list member must yield the same components as the same citation written primary.

    Found at corpus scale: ``§§ 154(i), 4(i)`` folded ``(i)`` into the *section* for the
    continuation items while the primary split it into ``parsed_subsection`` — so one
    provision produced two different edges (``4`` vs ``4(i)``).
    """
    mentions = detect_mentions("under 47 U.S.C. §§ 154(i), 4(i), and 303(r)")
    assert [(m.parsed.parsed_section, m.parsed.parsed_subsection) for m in mentions] == [
        ("154", "(i)"), ("4", "(i)"), ("303", "(r)"),
    ]
    # The primary form of the same member agrees.
    solo = detect_mentions("47 U.S.C. 4(i)")[0].parsed
    assert (solo.parsed_section, solo.parsed_subsection) == ("4", "(i)")
    # The raw span still quotes the text verbatim, subsection included.
    assert mentions[1].raw_reference_text == "4(i)"


def test_cfr_list_member_keeps_parenthesised_material_in_the_section():
    """CFR is the deliberate opposite: the dataset stores parens *inside* section_number."""
    mentions = detect_mentions("see 17 C.F.R. §§ 240.10b-5, 240.13a-1")
    assert [m.parsed.parsed_section for m in mentions] == ["240.10b-5", "240.13a-1"]
    assert all(m.parsed.parsed_subsection is None for m in mentions)


def test_title_range_guard_rejects_impossible_titles():
    """USC has 54 titles, the CFR 50. A citation naming a title outside its code's range
    cannot refer to real law, so the grammar abstains rather than emitting it.

    Every case here is a real detection from the v2026.08 federal corpus, where the digits
    adjacent to the code token came from a flattened table cell, a date column, a dollar
    amount, or a body whose leading digit was dropped at a line break.
    """
    for corpus_max, text in (
        (54, "Pub. L. 95-147 U.S.C. 19"),        # a Public Law number absorbed
        (54, "$122,661\nU.S.C. 362(a)"),          # a dollar amount from the next column
        (54, "479 U.S.C. 238 (1986)"),            # a U.S. Reports case cite
        (50, "on January 3, 2023\nCFR 2.2"),      # a date column
        (50, "Implementation\n0 CFR 264.100"),    # leading digit dropped (really 40 CFR)
    ):
        assert detect_mentions(text) == [], f"should abstain: {text!r}"
        assert corpus_max in (50, 54)

    # The boundaries themselves are valid and still parse.
    assert parse_citation("54 U.S.C. 100101") is not None
    assert parse_citation("50 CFR 17.11") is not None
    assert parse_citation("55 U.S.C. 1") is None
    assert parse_citation("51 CFR 17.11") is None


def test_title_range_is_a_model_invariant_not_only_a_parser_rule():
    """Direct construction is rejected too, so no producer can route around the guard."""
    with pytest.raises(ValueError, match="no title 147"):
        ParsedCitation(
            parsed_corpus=FederalCorpus.USC, parsed_title="147", parsed_section="19",
            reference_type=ReferenceType.ABSOLUTE, parser_method="usc_grammar_v1",
            parser_confidence=1.0,
        )
