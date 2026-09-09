from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

from open_us_law_citation.coverage_baseline import (
    TITLE_MAX,
    CurrencyStatus,
    DatasetCandidate,
    DatasetEvidence,
    FederalCorpus,
    OfficialInventory,
    OfficialProvision,
    ProvisionKey,
    StructuralStatus,
    TextAgreement,
    TitleCurrency,
    baseline_manifest,
    build_baseline,
    coverage_counts,
    coverage_rates,
    inventory_from_xml,
    load_official_inventory,
    oracle_source_sha256,
    render_manifest_json,
    render_markdown,
    render_official_inventory,
    text_fingerprints,
    title_in_range,
)
from open_us_law_citation.coverage_baseline import (
    main as coverage_main,
)
from open_us_law_citation.oracle_manifest import CutoffStatus, OracleKind

SHA_A = "a" * 64
SHA_B = "b" * 64


def _official(
    corpus: FederalCorpus,
    section: str,
    text: str | None,
    *,
    title: str = "1",
) -> OfficialProvision:
    return OfficialProvision.from_text(
        key=ProvisionKey(corpus, title, section),
        official_id=f"official-{title}-{section}",
        source_url=f"https://official.example/title-{title}/section-{section}",
        text=text,
    )


def _candidate(
    corpus: FederalCorpus,
    section: str,
    text: str | None,
    *,
    ordinal: int,
    title: str = "1",
) -> DatasetCandidate:
    raw_hash, normalized_hash = text_fingerprints(text)
    return DatasetCandidate(
        key=ProvisionKey(corpus, title, section),
        source_record_id=f"srr:test:{ordinal:04d}",
        act_id=f"{corpus.upper()}_{title}_{section}_{ordinal}",
        source_url=None,
        raw_text_sha256=raw_hash,
        normalized_text_sha256=normalized_hash,
    )


def _inventory(
    corpus: FederalCorpus,
    provisions: tuple[OfficialProvision, ...],
    *,
    cutoff: str = "2026-01-01",
) -> OfficialInventory:
    titles = sorted({item.key.title for item in provisions}, key=int)
    return OfficialInventory(
        corpus=corpus,
        oracle_edition=f"oracle:test:{corpus}:2026-01-01",
        oracle_kind=OracleKind.USLM if corpus == FederalCorpus.USC else OracleKind.ECFR,
        edition_date="2026-01-01",
        source_url="https://official.example/source.xml",
        source_sha256=SHA_A,
        title_currency=tuple(
            TitleCurrency(title, cutoff, "hermetic official fixture") for title in titles
        ),
        provisions=provisions,
    )


def _evidence(*, cutoff: str | None = "2026-01-01") -> DatasetEvidence:
    return DatasetEvidence(
        snapshot="v-test",
        dataset_revision="revision-test",
        source_file="federal.parquet",
        source_file_sha256=SHA_B,
        legal_content_cutoff=cutoff,
        cutoff_status=(
            CutoffStatus.ESTABLISHED if cutoff is not None else CutoffStatus.UNRESOLVED
        ),
    )


def test_crosswalk_reports_zero_one_and_multiple_candidates_without_coercion():
    corpus = FederalCorpus.CFR
    official = (
        _official(corpus, "1.1", "Exact text"),
        _official(corpus, "1.2", "Absent text"),
        _official(corpus, "1.3", "Duplicate text"),
        _official(corpus, "1.4", "Ambiguous text"),
        _official(corpus, "1.5", "same spacing"),
    )
    candidates = (
        _candidate(corpus, "1.1", "Exact text", ordinal=1),
        _candidate(corpus, "1.3", "Duplicate text", ordinal=2),
        _candidate(corpus, "1.3", "Duplicate text", ordinal=3),
        _candidate(corpus, "1.4", "candidate A", ordinal=4),
        _candidate(corpus, "1.4", "candidate B", ordinal=5),
        _candidate(corpus, "1.5", "same   spacing\n", ordinal=6),
        _candidate(corpus, "9.9", "dataset only", ordinal=7),
    )
    baseline = build_baseline(
        _inventory(corpus, official),
        inventory_sha256="c" * 64,
        candidates=candidates,
        dataset=_evidence(),
    )
    entries = {entry.key.section: entry for entry in baseline.entries}

    assert entries["1.1"].structural_status == StructuralStatus.REPRESENTED
    assert entries["1.1"].text_agreement == TextAgreement.EXACT
    assert entries["1.2"].structural_status == StructuralStatus.MISSING
    assert entries["1.3"].structural_status == StructuralStatus.DUPLICATE
    assert entries["1.3"].text_agreement == TextAgreement.PENDING_CFR_ASSEMBLY
    assert entries["1.4"].structural_status == StructuralStatus.AMBIGUOUS
    assert entries["1.4"].text_agreement == TextAgreement.PENDING_CFR_ASSEMBLY
    assert entries["1.5"].text_agreement == TextAgreement.NORMALIZED_ONLY
    assert entries["9.9"].structural_status == StructuralStatus.UNEXPECTED

    counts = baseline_manifest(baseline)["totals"]
    assert counts == {
        "expected": 5,
        "represented": 2,
        "missing": 1,
        "reserved": 0,
        "stale": 0,
        "duplicate": 1,
        "ambiguous": 1,
        "unexpected": 1,
        "exact_text": 1,
        "normalized_text": 2,
        "normalized_only_text": 1,
        "mismatch_text": 0,
        "pending_text": 2,
        "unavailable_text": 1,
        "aligned_currency": 4,
        "ahead_of_oracle_currency": 0,
        "pending_currency": 0,
        "not_applicable_currency": 2,
    }
    assert baseline_manifest(baseline)["rates"]["represented_percent"] == "40.0000"


def test_currency_and_usc_anatomy_are_independent_pending_dimensions():
    provision = _official(FederalCorpus.USC, "101", "official operative text")
    candidate = _candidate(
        FederalCorpus.USC,
        "101",
        "official operative text\nEditorial Notes: ...",
        ordinal=1,
    )
    stale = build_baseline(
        _inventory(FederalCorpus.USC, (provision,), cutoff="2026-01-02"),
        inventory_sha256="c" * 64,
        candidates=(candidate,),
        dataset=_evidence(cutoff="2026-01-01"),
    ).entries[0]
    assert stale.structural_status == StructuralStatus.REPRESENTED
    assert stale.currency_status == CurrencyStatus.STALE
    assert stale.text_agreement == TextAgreement.PENDING_USC_ANATOMY

    unresolved = build_baseline(
        _inventory(FederalCorpus.USC, (provision,)),
        inventory_sha256="c" * 64,
        candidates=(candidate,),
        dataset=_evidence(cutoff=None),
    ).entries[0]
    assert unresolved.currency_status == CurrencyStatus.PENDING


def test_outputs_are_byte_stable_under_input_order_changes():
    official = (
        _official(FederalCorpus.CFR, "2.10", "ten"),
        _official(FederalCorpus.CFR, "2.2", "two"),
    )
    candidates = (
        _candidate(FederalCorpus.CFR, "2.2", "two", ordinal=2),
        _candidate(FederalCorpus.CFR, "2.10", "ten", ordinal=1),
    )
    first = build_baseline(
        _inventory(FederalCorpus.CFR, official),
        inventory_sha256="c" * 64,
        candidates=candidates,
        dataset=_evidence(),
    )
    second = build_baseline(
        _inventory(FederalCorpus.CFR, tuple(reversed(official))),
        inventory_sha256="c" * 64,
        candidates=reversed(candidates),
        dataset=_evidence(),
    )
    assert render_manifest_json(first) == render_manifest_json(second)
    assert render_markdown(first) == render_markdown(second)


def test_official_inventory_round_trips_as_hash_only_json(tmp_path: Path):
    inventory = _inventory(
        FederalCorpus.USC,
        (_official(FederalCorpus.USC, "1983", "Every person...", title="42"),),
    )
    path = tmp_path / "inventory.json"
    rendered = render_official_inventory(inventory)
    path.write_text(rendered)
    loaded = load_official_inventory(path)
    assert loaded == inventory
    assert "Every person" not in rendered
    assert render_official_inventory(loaded) == rendered


def test_uslm_xml_projection_extracts_sections_and_title_currency(tmp_path: Path):
    source = tmp_path / "usc42.xml"
    source.write_text(
        """<uscDoc xmlns=\"http://xml.house.gov/schemas/uslm/1.0\">
        <meta><docNumber>Title 42</docNumber></meta>
        <main><section id=\"s1983\"><num value=\"1983\">§ 1983.</num>
        <heading>Civil action</heading><content>Every person...</content>
        </section></main></uscDoc>"""
    )
    checksum = hashlib.sha256(source.read_bytes()).hexdigest()
    inventory = inventory_from_xml(
        source_path=source,
        corpus=FederalCorpus.USC,
        oracle_edition="oracle:test:uslm",
        oracle_kind=OracleKind.USLM,
        edition_date="2025-01-06",
        source_url="https://official.example/usc.xml",
        source_sha256=checksum,
        currency_basis="release point through Public Law test",
    )
    assert [(item.key.title, item.key.section) for item in inventory.provisions] == [
        ("42", "1983")
    ]
    assert inventory.title_currency == (
        TitleCurrency("42", "2025-01-06", "release point through Public Law test"),
    )


def test_ecfr_xml_projection_extracts_only_section_divisions(tmp_path: Path):
    source = tmp_path / "title-17.xml"
    source.write_text(
        """<ECFR TITLE=\"17\"><DIV5 TYPE=\"PART\" N=\"240\">
        <DIV8 TYPE=\"SECTION\" N=\"§ 240.10b-5\" ID=\"se17.4.240_110b_65\">
        <HEAD>§ 240.10b-5 Employment of manipulative practices.</HEAD>
        <P>It shall be unlawful...</P></DIV8></DIV5></ECFR>"""
    )
    checksum = hashlib.sha256(source.read_bytes()).hexdigest()
    inventory = inventory_from_xml(
        source_path=source,
        corpus=FederalCorpus.CFR,
        oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR,
        edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256=checksum,
        currency_basis="point-in-time eCFR fixture",
    )
    assert len(inventory.provisions) == 1
    provision = inventory.provisions[0]
    assert provision.key == ProvisionKey(FederalCorpus.CFR, "17", "240.10b-5")
    assert provision.source_url == "https://official.example/title-17.xml"


def test_inventory_rejects_wrong_source_checksum(tmp_path: Path):
    source = tmp_path / "usc01.xml"
    source.write_text("<uscDoc />")
    with pytest.raises(ValueError, match="checksum differs"):
        inventory_from_xml(
            source_path=source,
            corpus=FederalCorpus.USC,
            oracle_edition="oracle:test:uslm",
            oracle_kind=OracleKind.USLM,
            edition_date="2025-01-06",
            source_url="https://official.example/usc.xml",
            source_sha256=SHA_A,
            currency_basis="fixture",
        )


def test_directory_source_hash_binds_paths_and_unmodified_xml_bytes(tmp_path: Path):
    source = tmp_path / "ecfr"
    source.mkdir()
    (source / "title-1.xml").write_text("<ECFR TITLE=\"1\" />")
    (source / "title-2.xml").write_text("<ECFR TITLE=\"2\" />")
    first, method = oracle_source_sha256(source)
    assert method == "sha256_tree_v1"
    assert len(first) == 64

    (source / "title-2.xml").write_text("<ECFR TITLE=\"2\"><!-- changed --></ECFR>")
    second, _ = oracle_source_sha256(source)
    assert second != first


def test_official_inventory_requires_currency_for_every_title():
    inventory = _inventory(
        FederalCorpus.USC,
        (_official(FederalCorpus.USC, "1983", "text", title="42"),),
    )
    with pytest.raises(ValueError, match="lacks title-level currency"):
        replace(inventory, title_currency=())


def test_empty_official_inventory_cannot_be_used_as_a_denominator():
    with pytest.raises(ValueError, match="at least one provision"):
        OfficialInventory(
            corpus=FederalCorpus.USC,
            oracle_edition="oracle:test:empty",
            oracle_kind=OracleKind.USLM,
            edition_date="2026-01-01",
            source_url="https://official.example/empty.xml",
            source_sha256=SHA_A,
            title_currency=(),
            provisions=(),
        )


def test_cli_refuses_to_build_from_an_unstaged_oracle(tmp_path: Path):
    with pytest.raises(SystemExit, match="is not staged"):
        coverage_main(
            [
                "build-inventory",
                "--corpus",
                "usc",
                "--oracle-manifest",
                "oracles/v2026.08.json",
                "--currency-basis",
                "fixture",
                "--output",
                str(tmp_path / "must-not-exist.json"),
            ]
        )
    assert not (tmp_path / "must-not-exist.json").exists()


def _reserved_official(section: str, *, title: str = "1") -> OfficialProvision:
    return OfficialProvision.from_text(
        key=ProvisionKey(FederalCorpus.CFR, title, section),
        official_id=f"official-{title}-{section}",
        source_url=f"https://official.example/title-{title}/section-{section}",
        text=f"§ {section}   [Reserved]",
        reserved=True,
    )


def test_ecfr_projection_marks_reserved_sections_including_the_trailing_period(
    tmp_path: Path,
):
    """eCFR marks reserved ONLY in <HEAD>; there is no RESERVED attribute.

    The trailing-period variant is real: at the 2026-08-26 edition, 23 CFR 1270.5 is an
    empty `[Reserved].` placeholder that the eCFR *structure API* reports as NOT reserved.
    The XML is right, so the head match must tolerate it. A reserved element also often
    spans a whole range of numbers in one element.
    """
    source = tmp_path / "title-3.xml"
    source.write_text(
        """<ECFR TITLE="3"><DIV5 TYPE="PART" N="102">
        <DIV8 TYPE="SECTION" N="102.1"><HEAD>§ 102.1 Purpose.</HEAD>
        <P>This part governs...</P></DIV8>
        <DIV8 TYPE="SECTION" N="102.104-102.109">
        <HEAD>§§ 102.104-102.109   [Reserved]</HEAD></DIV8>
        <DIV8 TYPE="SECTION" N="1270.5"><HEAD>§ 1270.5   [Reserved].</HEAD></DIV8>
        </DIV5></ECFR>"""
    )
    inventory = inventory_from_xml(
        source_path=source,
        corpus=FederalCorpus.CFR,
        oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR,
        edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        currency_basis="point-in-time eCFR fixture",
    )
    by_section = {p.key.section: p for p in inventory.provisions}
    assert by_section["102.1"].reserved is False
    assert by_section["102.104-102.109"].reserved is True   # range in one element
    assert by_section["1270.5"].reserved is True            # trailing period


def test_reserved_is_its_own_stratum_and_is_held_out_of_the_denominator():
    """A reserved section is an empty official placeholder -- neither present nor absent
    law -- so it must not be scored `missing` and must not sit in `expected`."""
    inventory = OfficialInventory(
        corpus=FederalCorpus.CFR,
        oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR,
        edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256="a" * 64,
        title_currency=(TitleCurrency("1", "2026-08-26", "point-in-time eCFR fixture"),),
        provisions=(
            _official(FederalCorpus.CFR, "1.1", "present law"),
            _official(FederalCorpus.CFR, "1.2", "absent law"),
            _reserved_official("1.3-1.9"),
        ),
    )
    dataset = _evidence()
    baseline = build_baseline(
        inventory=inventory,
        inventory_sha256="b" * 64,
        dataset=dataset,
        candidates=[_candidate(FederalCorpus.CFR, "1.1", "present law", ordinal=1)],
    )
    by_section = {e.key.section: e for e in baseline.entries}
    assert by_section["1.1"].structural_status == StructuralStatus.REPRESENTED
    assert by_section["1.2"].structural_status == StructuralStatus.MISSING
    assert by_section["1.3-1.9"].structural_status == StructuralStatus.RESERVED

    counts = coverage_counts(baseline.entries)
    # The reserved placeholder is NOT in the denominator and NOT counted missing.
    assert counts["expected"] == 2
    assert counts["reserved"] == 1
    assert counts["missing"] == 1
    # ... so coverage is 1/2, not 1/3.
    assert coverage_rates(counts)["represented_percent"] == "50.0000"
    # A reserved section has no operative text, so it enters no text bucket.
    assert counts["exact_text"] + counts["mismatch_text"] + counts["unavailable_text"] == 2


def test_reserved_stays_reserved_even_when_the_dataset_carries_a_row():
    """Classification follows the *official* source: if it publishes no law at the key,
    a dataset row there does not make it `represented`."""
    inventory = OfficialInventory(
        corpus=FederalCorpus.CFR,
        oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR,
        edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256="a" * 64,
        title_currency=(TitleCurrency("1", "2026-08-26", "point-in-time eCFR fixture"),),
        provisions=(_reserved_official("1.5"),),
    )
    baseline = build_baseline(
        inventory=inventory,
        inventory_sha256="b" * 64,
        dataset=_evidence(),
        candidates=[_candidate(FederalCorpus.CFR, "1.5", "stale text", ordinal=1)],
    )
    assert baseline.entries[0].structural_status == StructuralStatus.RESERVED
    counts = coverage_counts(baseline.entries)
    assert counts["expected"] == 0 and counts["reserved"] == 1
    assert coverage_rates(counts)["represented_percent"] is None


def test_ecfr_section_number_comes_from_N_never_from_the_heading(tmp_path: Path):
    """`N` is authoritative and present on 100% of real section elements (54,129 of 54,129
    across staged titles 1-16 at the 2026-08-26 edition).

    A regex over the `<HEAD>` used to be the fallback. On that same real sample it would
    have disagreed with `N` on 20 elements — the heads below are three of them. A key like
    `752.1.` matches no dataset row, so the provision would have scored `missing` because
    of a punctuation mark.
    """
    source = tmp_path / "title-12.xml"
    source.write_text(
        """<ECFR TITLE="12"><DIV5 TYPE="PART" N="752">
        <DIV8 TYPE="SECTION" N="752.1"><HEAD>§ 752.1.   What is the scope.</HEAD>
        <P>Text.</P></DIV8>
        <DIV8 TYPE="SECTION" N="120.441-§ 120.447"><HEAD>§ 120.441-§ 120.447   [Reserved]</HEAD></DIV8>
        <DIV8 TYPE="SECTION" N="1777.5 through 1777.10">
        <HEAD>§§ 1777.5 through 1777.10   [Reserved]</HEAD></DIV8>
        </DIV5></ECFR>"""
    )
    inventory = inventory_from_xml(
        source_path=source, corpus=FederalCorpus.CFR, oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR, edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        currency_basis="point-in-time eCFR fixture",
    )
    sections = [p.key.section for p in inventory.provisions]
    # Exactly N, with no trailing period, no captured section sign, no truncated range.
    assert sections == ["752.1", "120.441-§ 120.447", "1777.5 through 1777.10"]


def test_a_section_element_without_N_fails_loudly_instead_of_being_skipped(tmp_path: Path):
    """The old fallback could yield nothing, and the element was then silently skipped —
    dropping a section out of the coverage denominator with nothing saying so."""
    source = tmp_path / "title-9.xml"
    source.write_text(
        """<ECFR TITLE="9"><DIV5 TYPE="PART" N="1">
        <DIV8 TYPE="SECTION"><HEAD>§ 1.1   Scope.</HEAD><P>Text.</P></DIV8>
        </DIV5></ECFR>"""
    )
    with pytest.raises(ValueError, match="no N attribute"):
        inventory_from_xml(
            source_path=source, corpus=FederalCorpus.CFR, oracle_edition="oracle:test:ecfr",
            oracle_kind=OracleKind.ECFR, edition_date="2026-08-26",
            source_url="https://official.example/title-{title}.xml",
            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            currency_basis="point-in-time eCFR fixture",
        )


def test_uslm_docnumber_title_is_bounded_by_the_real_title_range(tmp_path: Path):
    """The USC has 54 titles, so a docNumber digit run outside 1-54 is not a title.

    Accepting one would anchor every provision in the file to a denominator key that
    cannot exist. Not yet validated against real USLM bytes (OLRC unreachable), so this
    pins the bound rather than the extraction.
    """
    source = tmp_path / "unnamed.xml"   # filename carries no title -> docNumber fallback
    source.write_text(
        """<uscDoc xmlns="http://xml.house.gov/schemas/uslm/1.0">
        <meta><docNumber>118</docNumber></meta>
        <section><num value="1">§ 1.</num><content>Text.</content></section>
        </uscDoc>"""
    )
    with pytest.raises(ValueError, match="cannot determine USC title"):
        inventory_from_xml(
            source_path=source, corpus=FederalCorpus.USC, oracle_edition="oracle:test:uslm",
            oracle_kind=OracleKind.USLM, edition_date="2025-01-06",
            source_url="https://official.example/usc.zip",
            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            currency_basis="USLM fixture",
        )


def test_title_range_has_one_definition_shared_with_the_m2_grammar():
    """A citation and an oracle key must not disagree about what a valid title is."""
    from open_us_law_citation.citation_parser import TITLE_MAX as grammar_max

    assert grammar_max is TITLE_MAX
    assert title_in_range(FederalCorpus.USC, "54") and not title_in_range(FederalCorpus.USC, "55")
    assert title_in_range(FederalCorpus.CFR, "50") and not title_in_range(FederalCorpus.CFR, "51")
