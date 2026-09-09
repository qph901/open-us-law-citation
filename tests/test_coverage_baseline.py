from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

from open_us_law_citation.coverage_baseline import (
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
    inventory_from_xml,
    load_official_inventory,
    oracle_source_sha256,
    render_manifest_json,
    render_markdown,
    render_official_inventory,
    text_fingerprints,
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
