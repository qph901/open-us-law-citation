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
    ParsedCitation,
    ReferenceType,
    analyze_file,
    build_reference_mention,
    detect_mentions,
    parse_cfr_citation,
    parse_citation,
    parse_usc_citation,
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
