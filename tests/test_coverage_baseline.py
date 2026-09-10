from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from open_us_law_citation.coverage_baseline import (
    _ECFR_RESERVED_BODY_RE,
    _ECFR_RESERVED_RE,
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
    scan_dataset_candidates,
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
        "empty_official_body": 0,
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
    dated = replace(provision, official_amendment_date="2026-01-02")
    stale = build_baseline(
        _inventory(FederalCorpus.USC, (dated,), cutoff="2026-01-02"),
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


def _reference_candidates(path, *, snapshot, corpus):
    """The pre-DuckDB implementation, kept here as the oracle for the differential test."""
    from open_us_law_citation.coverage_baseline import DatasetCandidate
    from open_us_law_citation.source_record import iter_source_records

    out = []
    for record in iter_source_records(path, snapshot):
        act_id = record.column("act_id") or ""
        if corpus == FederalCorpus.CFR and act_id.startswith("FR_"):
            continue
        if not act_id.startswith("USC_" if corpus == FederalCorpus.USC else "CFR_"):
            continue
        out.append(DatasetCandidate.from_source_record(record, corpus))
    return out


def _federal_fixture(path, rows):
    """A real-shaped 24-column file: canonical column order and Arrow types."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    from open_us_law_citation.source_record import EXPECTED_COLUMNS

    ints = {"word_count", "last_amended_year", "subsection_count", "year"}
    schema = pa.schema(
        [pa.field(n, pa.int64() if n in ints else pa.string()) for n in EXPECTED_COLUMNS]
    )
    cols = {n: [r.get(n) for r in rows] for n in EXPECTED_COLUMNS}
    pq.write_table(pa.table(cols, schema=schema), path, row_group_size=2)


_FED_ROWS = [
    {"act_id": "CFR_T1_S1", "section_number": "1.0", "title_number": "1",
     "source_url": "https://e.example/0", "text": "Body A"},
    {"act_id": "CFR_T1_S2", "section_number": "1.1", "title_number": "1",
     "source_url": "https://e.example/1", "text": "Body B"},
    {"act_id": "FR_DOC_1", "section_number": "1.2", "title_number": "1",
     "source_url": "https://e.example/2", "text": "FR body"},
    {"act_id": "CFR_T1_S3", "section_number": "1.3", "title_number": "1",
     "source_url": "https://e.example/3", "text": None},
    {"act_id": "USC_T1_S9", "section_number": "9", "title_number": "1",
     "source_url": "https://e.example/4", "text": "USC body"},
    {"act_id": "CFR_T1_S4", "section_number": "1.5", "title_number": "1",
     "source_url": "https://e.example/5", "text": ""},
    {"act_id": "CFR_T1_S5", "section_number": "1.6", "title_number": "1",
     "source_url": "https://e.example/6", "text": "Body C"},
]


def test_duckdb_candidate_scan_matches_the_row_group_reader_exactly(tmp_path: Path):
    """`scan_dataset_candidates` streams through DuckDB because `iter_source_records`
    reads a whole row group with no column projection — row group 24 of
    us_federal_regulations.parquet is 3.10 GB of text and peaks over 5.9 GB, OOM-killing a
    14 GB box (measured), and that is exactly the file COV-1A's CFR half runs on.

    Changing the engine must not change identity: `source_record_id` derives from the
    physical row ordinal, so DuckDB's `file_row_number` has to equal what the row-group
    reader assigns. This asserts the two paths agree candidate-for-candidate, across row
    group boundaries (the fixture has several).
    """
    path = tmp_path / "fed.parquet"
    _federal_fixture(path, _FED_ROWS)

    got, evidence = scan_dataset_candidates(
        path, snapshot="v-test", dataset_revision="rev", corpus=FederalCorpus.CFR,
        legal_content_cutoff="2026-01-01", cutoff_status=CutoffStatus.ESTABLISHED,
    )
    want = _reference_candidates(path, snapshot="v-test", corpus=FederalCorpus.CFR)

    assert [c.source_record_id for c in got] == [c.source_record_id for c in want]
    assert [c.key for c in got] == [c.key for c in want]
    assert [c.raw_text_sha256 for c in got] == [c.raw_text_sha256 for c in want]
    assert [c.normalized_text_sha256 for c in got] == [c.normalized_text_sha256 for c in want]
    assert [c.source_url for c in got] == [c.source_url for c in want]
    assert evidence.excluded_federal_register_rows == 1      # FR excluded from CFR
    assert evidence.excluded_other_rows == 1                 # the USC row
    # A null body and an empty body must not share a fingerprint.
    raw = [c.raw_text_sha256 for c in got]
    assert None in raw and len({h for h in raw if h}) == len([h for h in raw if h])


def test_candidate_scan_rejects_a_file_with_the_wrong_schema(tmp_path: Path):
    """Streaming skips iter_source_records, so the 24-column gate had to be restored here;
    without it an off-schema file would flow into a coverage claim unchecked."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    path = tmp_path / "bad.parquet"
    pq.write_table(pa.table({"act_id": pa.array(["CFR_T1_S1"]), "text": pa.array(["x"])}), path)
    with pytest.raises(Exception, match="24-column"):
        scan_dataset_candidates(
            path, snapshot="v-test", dataset_revision="rev", corpus=FederalCorpus.CFR,
            legal_content_cutoff=None, cutoff_status=CutoffStatus.UNRESOLVED,
        )


def test_candidate_scan_still_verifies_the_dataset_checksum(tmp_path: Path):
    """The checksum gate moved with the reader; losing it would let unverified bytes into
    a coverage claim."""
    path = tmp_path / "fed.parquet"
    _federal_fixture(path, _FED_ROWS[:1])
    with pytest.raises(ValueError, match="checksum mismatch"):
        scan_dataset_candidates(
            path, snapshot="v-test", dataset_revision="rev", corpus=FederalCorpus.CFR,
            expected_sha256="f" * 64,
            legal_content_cutoff=None, cutoff_status=CutoffStatus.UNRESOLVED,
        )


def test_null_cfr_title_is_recovered_from_act_id_and_counted(tmp_path: Path):
    """CLAUDE.md records the flat hierarchy columns as unreliable, and `title_number` is
    null on 1,703 of the 220,018 real CFR rows — the first at physical row 63, which
    aborted the whole scan before this.

    `act_id` encodes the title unambiguously (`CFR_T10_P54_S54_17` -> 10), so this is
    recovery from a more reliable field, not a guess. It is counted rather than silent:
    how far the flat columns can be trusted is itself a coverage-relevant fact.
    """
    rows = [
        {"act_id": "CFR_T10_P54_S54_17", "section_number": "54.17", "title_number": None,
         "source_url": "https://e.example/a", "text": "Body"},
        {"act_id": "CFR_T1_S1", "section_number": "1.1", "title_number": "1",
         "source_url": "https://e.example/b", "text": "Body"},
    ]
    path = tmp_path / "fed.parquet"
    _federal_fixture(path, rows)
    got, evidence = scan_dataset_candidates(
        path, snapshot="v-test", dataset_revision="rev", corpus=FederalCorpus.CFR,
        legal_content_cutoff=None, cutoff_status=CutoffStatus.UNRESOLVED,
    )
    assert [c.key.title for c in got] == ["10", "1"]
    assert evidence.recovered_title_rows == 1


def test_an_unrecoverable_row_still_fails_loudly(tmp_path: Path):
    """Recovery is not a licence to invent: an act_id that carries no title must raise,
    not silently drop the row out of the dataset side and inflate `missing`."""
    rows = [{"act_id": "CFR_NOTATITLE", "section_number": "1.1", "title_number": None,
             "source_url": None, "text": "Body"}]
    path = tmp_path / "fed.parquet"
    _federal_fixture(path, rows)
    with pytest.raises(ValueError, match="lacks title/section/act_id"):
        scan_dataset_candidates(
            path, snapshot="v-test", dataset_revision="rev", corpus=FederalCorpus.CFR,
            legal_content_cutoff=None, cutoff_status=CutoffStatus.UNRESOLVED,
        )


def test_title_recovery_pattern_is_anchored_to_canonical_cfr_act_ids():
    from open_us_law_citation.coverage_baseline import _CFR_TITLE_FROM_ACT_ID

    assert _CFR_TITLE_FROM_ACT_ID.match("CFR_T10_P54_S54_17").group(1) == "10"
    assert _CFR_TITLE_FROM_ACT_ID.match("CFR_T5_P1_S1_1").group(1) == "5"
    # Negative cases: it must not fire on anything but a canonical CFR act_id.
    for bad in ("FR_PRORULE_2025-06180", "USC_T42_C21_S1983", "XCFR_T10_P1",
                "CFR_P54_S54_17", "CFR_TX_P1", "CFR_T10"):
        assert _CFR_TITLE_FROM_ACT_ID.match(bad) is None, bad


@pytest.mark.parametrize(
    "filename,expected",
    [
        # The convention the repo's own fixtures assume. NOT verified against a real OLRC
        # release point -- uscode.house.gov has been unreachable throughout this work.
        ("usc01.xml", "1"),
        ("usc42.xml", "42"),
        ("usc54.xml", "54"),            # the highest real title
        ("uscode05.xml", "5"),
        ("usc_10.xml", "10"),
        ("usc-10.xml", "10"),
        # Out of range -> None, so the caller falls back to <docNumber> rather than
        # anchoring a document to a title that cannot exist.
        ("usc55.xml", None),
        ("usc00.xml", None),
        ("usc999.xml", None),
        # Not a USC filename at all.
        ("title-3.xml", None),
        ("readme.xml", None),
    ],
)
def test_uslm_title_from_filename(filename, expected):
    from open_us_law_citation.coverage_baseline import _title_from_name

    assert _title_from_name(filename, FederalCorpus.USC) == expected


def test_uslm_appendix_filename_resolves_to_the_bare_title():
    """`usc05A.xml` yields "5", the same as `usc05.xml`.

    Recorded as observed behaviour, not endorsed: whether OLRC names appendices this way
    is unverified here. It is precisely why `_reject_repeated_title` exists — the merge it
    would otherwise cause is silent, since appendix sections do not collide with title 5's.
    """
    from open_us_law_citation.coverage_baseline import _title_from_name

    assert _title_from_name("usc05A.xml", FederalCorpus.USC) == "5"
    assert _title_from_name("usc05.xml", FederalCorpus.USC) == "5"


def test_two_documents_claiming_one_title_is_refused(tmp_path: Path):
    """The silent failure this prevents: two files merging into one title's denominator."""
    source = tmp_path / "ecfr"
    source.mkdir()
    for name in ("title-3.xml", "title-3-appendix.xml"):
        (source / name).write_text(
            """<ECFR TITLE="3"><DIV5 TYPE="PART" N="100">
            <DIV8 TYPE="SECTION" N="100.1"><HEAD>§ 100.1 A.</HEAD><P>x</P></DIV8>
            </DIV5></ECFR>""".replace("100.1", "100.1" if name == "title-3.xml" else "200.9")
        )
    with pytest.raises(ValueError, match="both resolve to title 3"):
        inventory_from_xml(
            source_path=source, corpus=FederalCorpus.CFR, oracle_edition="oracle:test:ecfr",
            oracle_kind=OracleKind.ECFR, edition_date="2026-08-26",
            source_url="https://official.example/title-{title}.xml",
            source_sha256=oracle_source_sha256(source)[0],
            currency_basis="point-in-time eCFR fixture",
        )


def test_ecfr_title_from_filename_matches_every_staged_file():
    """The eCFR half IS verified against real bytes: every staged title-N.xml resolves."""
    import glob

    from open_us_law_citation.coverage_baseline import _title_from_name

    staged = sorted(glob.glob("data/oracles/ecfr-2026-08-26/title-*.xml"))
    if not staged:
        pytest.skip("no staged eCFR edition present")
    for path in staged:
        name = Path(path).name
        expected = name.removeprefix("title-").removesuffix(".xml")
        assert _title_from_name(name, FederalCorpus.CFR) == expected


def test_ecfr_operative_text_excludes_the_section_heading(tmp_path: Path):
    """The heading is metadata — the section number is already the provision key — and the
    Open US Law `text` column starts at the body.

    Including it made EVERY provision mismatch: measured over the staged edition, exact and
    normalized text agreement were both 0.00% across 113,224 represented provisions.
    Excluding it took them to 65.57% and 69.73%. A reported 0% would have read as
    catastrophic coverage failure when it was a projection artifact.
    """
    source = tmp_path / "title-3.xml"
    source.write_text(
        """<ECFR TITLE="3"><DIV5 TYPE="PART" N="100">
        <DIV8 TYPE="SECTION" N="100.1"><HEAD>§ 100.1   Ethical conduct standards.</HEAD>
        <P>Employees are subject to the executive branch standards.</P></DIV8>
        </DIV5></ECFR>"""
    )
    inventory = inventory_from_xml(
        source_path=source, corpus=FederalCorpus.CFR, oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR, edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        currency_basis="point-in-time eCFR fixture",
    )
    provision = inventory.provisions[0]
    body_only, _ = text_fingerprints("Employees are subject to the executive branch standards.")
    with_heading, _ = text_fingerprints(
        "§ 100.1   Ethical conduct standards.\n"
        "Employees are subject to the executive branch standards."
    )
    assert provision.raw_text_sha256 == body_only
    assert provision.raw_text_sha256 != with_heading


def test_text_following_the_heading_is_kept():
    """Only the heading's own subtree is dropped — text that follows it in the parent must
    survive, or the fix would trade one systematic mismatch for another."""
    import xml.etree.ElementTree as ET

    from open_us_law_citation.coverage_baseline import (
        _direct_child,
        _flatten_xml_text_excluding,
    )

    element = ET.fromstring(
        '<DIV8 TYPE="SECTION" N="1.1"><HEAD>§ 1.1 Scope.</HEAD>tail after head'
        "<P>Body paragraph.</P></DIV8>"
    )
    head = _direct_child(element, "head")
    flattened = _flatten_xml_text_excluding(element, head)
    assert "Scope" not in flattened
    assert "tail after head" in flattened and "Body paragraph." in flattened


def test_excluding_a_missing_child_is_a_no_op():
    """A section element with no HEAD must still project its full body."""
    import xml.etree.ElementTree as ET

    from open_us_law_citation.coverage_baseline import _flatten_xml_text_excluding

    element = ET.fromstring('<DIV8 TYPE="SECTION" N="1.1"><P>Only a body.</P></DIV8>')
    assert _flatten_xml_text_excluding(element, None) == "Only a body."


def test_an_inventory_from_an_older_text_projection_is_refused(tmp_path: Path):
    """A saved inventory stores only hashes, so a stale one loads happily and silently
    reproduces the OLD projection's results.

    Concretely: v1 included the section heading in the operative text, which made exact
    and normalized agreement 0.00% across 113,224 provisions. Reusing a v1 inventory under
    v2 code would quietly report that 0% again, with nothing to indicate why.
    """
    source = tmp_path / "title-3.xml"
    source.write_text(
        """<ECFR TITLE="3"><DIV5 TYPE="PART" N="100">
        <DIV8 TYPE="SECTION" N="100.1"><HEAD>§ 100.1 Scope.</HEAD><P>Body.</P></DIV8>
        </DIV5></ECFR>"""
    )
    inventory = inventory_from_xml(
        source_path=source, corpus=FederalCorpus.CFR, oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR, edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        currency_basis="fixture",
    )
    saved = tmp_path / "inv.json"
    saved.write_text(render_official_inventory(inventory))
    assert load_official_inventory(saved).provisions[0].key.section == "100.1"

    # Downgrade the recorded projection, as a file written before the fix would carry.
    stale = json.loads(saved.read_text())
    stale["official_text_projection"] = "xml_text_nodes_newline_v1"
    saved.write_text(json.dumps(stale))
    with pytest.raises(ValueError, match="not comparable"):
        load_official_inventory(saved)


def test_reserved_survives_an_inventory_round_trip(tmp_path: Path):
    """Without serialising `reserved`, a reloaded inventory puts every empty placeholder
    back into `expected` to be scored `missing` — the gap the stratum exists to close."""
    source = tmp_path / "title-3.xml"
    source.write_text(
        """<ECFR TITLE="3"><DIV5 TYPE="PART" N="100">
        <DIV8 TYPE="SECTION" N="100.1"><HEAD>§ 100.1 Scope.</HEAD><P>Body.</P></DIV8>
        <DIV8 TYPE="SECTION" N="100.2-100.9"><HEAD>§§ 100.2-100.9   [Reserved]</HEAD></DIV8>
        </DIV5></ECFR>"""
    )
    inventory = inventory_from_xml(
        source_path=source, corpus=FederalCorpus.CFR, oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR, edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        currency_basis="fixture",
    )
    saved = tmp_path / "inv.json"
    saved.write_text(render_official_inventory(inventory))
    reloaded = load_official_inventory(saved)

    before = {p.key.section: p.reserved for p in inventory.provisions}
    after = {p.key.section: p.reserved for p in reloaded.provisions}
    assert before == after == {"100.1": False, "100.2-100.9": True}

    # And the reloaded inventory still holds reserved out of the denominator.
    baseline = build_baseline(
        inventory=reloaded, inventory_sha256="b" * 64, dataset=_evidence(),
        candidates=[_candidate(FederalCorpus.CFR, "100.1", "Body", ordinal=1, title="3")],
    )
    counts = coverage_counts(baseline.entries)
    assert counts["expected"] == 1 and counts["reserved"] == 1 and counts["missing"] == 0


# --- empty_official_body: the stratum, and the regex that feeds it -------------------


@pytest.mark.parametrize(
    "head",
    [
        "§ 1.8   [Reserved]",
        "§ 1270.5   [Reserved].",              # trailing period (structure API says no)
        "§ 83.28   [Reserved] (Rule 28).",     # trailing parenthetical
        "§§ 989.221-989.257 [Reserved",        # 7 CFR: no closing bracket
        "§ 93.323 [Reserved",                  # 14 CFR: no closing bracket
        "§ 176.142   Reserved]",               # 49 CFR: no opening bracket
        "§ 100.11 ]Reserved]",                 # 31 CFR: mistyped opening bracket
        "§ 80.149 {Reserved]",                 # 47 CFR: brace for bracket
    ],
)
def test_reserved_head_matches_every_real_bracket_typo(head: str):
    """All five malformed variants are real headings in the pinned CFR 2026-08-26 edition,
    each with an empty body. A strict `\\[reserved\\]` missed all five."""
    assert _ECFR_RESERVED_RE.search(head) is not None


@pytest.mark.parametrize(
    "head",
    [
        "§ 214.402 Career reserved positions.",           # 5 CFR
        "§ 4284.916 Reserved funds.",                     # 7 CFR
        "§ 4284.923 Reserved funds eligibility.",         # 7 CFR
        "§ 46.15 Documents to be preserved.",             # 7 CFR
        "§ 601.2 Functions reserved to the Secretary.",   # 7 CFR
        "§ 328.109 Other actions preserved.",             # 12 CFR
        "§ 2.23 Use of reserved authority in licenses.",  # 18 CFR
        "§ 240.17a-4 Records to be preserved [1997].",    # bracket, but not around it
        "Records to be preserved]",                       # `preserved]` must NOT match
        "[Records] to be preserved by brokers.",          # bracket far from the word
    ],
)
def test_reserved_head_rejects_law_that_merely_says_reserved(head: str):
    """61 headings in the same edition use these letters as law, not as a placeholder.
    Dropping the bracket to catch the typos would swallow every one of them, and the word
    boundary is what stops `preserved]` from matching."""
    assert _ECFR_RESERVED_RE.search(head) is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", True),
        ("   ", True),
        ("\n\n\t ", True),          # whitespace-only normalizes to "" exactly
        ("\xa0", True),            # str.split() treats NBSP as whitespace: empty
        ("law", False),
        (" law ", False),
        (None, False),              # text UNAVAILABLE is not text that is empty
    ],
)
def test_empty_body_is_derived_from_the_official_text(text: str | None, expected: bool):
    provision = OfficialProvision.from_text(
        key=ProvisionKey(FederalCorpus.CFR, "48", "1.105"),
        official_id="cfr-title-48-section-1.105",
        source_url="https://official.example/title-48.xml",
        text=text,
    )
    assert provision.empty_body is expected


def test_empty_body_cannot_be_asserted_against_the_stored_hash():
    """`empty_body` is a checkable property of the normalized hash, not a claim, so a
    directly-constructed provision cannot mark a section with law as empty."""
    with_law = OfficialProvision.from_text(
        key=ProvisionKey(FederalCorpus.CFR, "48", "1.106"),
        official_id="cfr-title-48-section-1.106",
        source_url="https://official.example/title-48.xml",
        text="Contracting authority.",
    )
    with pytest.raises(ValueError, match="empty_body"):
        replace(with_law, empty_body=True)
    empty = OfficialProvision.from_text(
        key=ProvisionKey(FederalCorpus.CFR, "48", "1.105"),
        official_id="cfr-title-48-section-1.105",
        source_url="https://official.example/title-48.xml",
        text="",
    )
    with pytest.raises(ValueError, match="empty_body"):
        replace(empty, empty_body=False)


def _empty_body_official(section: str, *, title: str = "48") -> OfficialProvision:
    return OfficialProvision.from_text(
        key=ProvisionKey(FederalCorpus.CFR, title, section),
        official_id=f"cfr-title-{title}-section-{section}",
        source_url=f"https://official.example/title-{title}.xml",
        text="",
    )


def _empty_body_inventory(*sections: str) -> OfficialInventory:
    return OfficialInventory(
        corpus=FederalCorpus.CFR,
        oracle_edition="oracle:test:ecfr",
        oracle_kind=OracleKind.ECFR,
        edition_date="2026-08-26",
        source_url="https://official.example/title-{title}.xml",
        source_sha256=SHA_A,
        title_currency=(TitleCurrency("48", "2026-08-26", "point-in-time eCFR fixture"),),
        provisions=(
            _official(FederalCorpus.CFR, "1.106", "Contracting authority.", title="48"),
            _official(FederalCorpus.CFR, "1.107", "Publication.", title="48"),
            *(_empty_body_official(s) for s in sections),
        ),
    )


def test_empty_official_body_is_held_out_of_the_denominator():
    """`48 CFR 1.105` is a heading with no body -- its law is in `1.105-1/-2/-3`, which the
    dataset carries. Scoring the parent `missing` invented a 1,469-section CFR gap."""
    baseline = build_baseline(
        inventory=_empty_body_inventory("1.105"),
        inventory_sha256=SHA_B,
        dataset=_evidence(),
        candidates=[
            _candidate(
                FederalCorpus.CFR, "1.106", "Contracting authority.", ordinal=1, title="48"
            )
        ],
    )
    by_section = {e.key.section: e for e in baseline.entries}
    assert by_section["1.105"].structural_status == StructuralStatus.EMPTY_OFFICIAL_BODY
    assert by_section["1.106"].structural_status == StructuralStatus.REPRESENTED
    assert by_section["1.107"].structural_status == StructuralStatus.MISSING

    counts = coverage_counts(baseline.entries)
    assert counts["empty_official_body"] == 1
    assert counts["expected"] == 2          # NOT 3
    assert counts["missing"] == 1           # NOT 2
    # ... so coverage is 1/2, not 1/3.
    assert coverage_rates(counts)["represented_percent"] == "50.0000"
    # An empty-bodied section has no operative text, so it enters no text bucket.
    assert counts["exact_text"] + counts["mismatch_text"] + counts["unavailable_text"] == 2


def test_empty_official_body_stays_held_out_when_the_dataset_carries_a_row():
    """Classification follows the *official* source, exactly as `reserved` does."""
    baseline = build_baseline(
        inventory=_empty_body_inventory("1.105"),
        inventory_sha256=SHA_B,
        dataset=_evidence(),
        candidates=[
            _candidate(FederalCorpus.CFR, "1.105", "surprise text", ordinal=1, title="48")
        ],
    )
    by_section = {e.key.section: e for e in baseline.entries}
    assert by_section["1.105"].structural_status == StructuralStatus.EMPTY_OFFICIAL_BODY
    counts = coverage_counts(baseline.entries)
    assert counts["expected"] == 2 and counts["empty_official_body"] == 1


def test_empty_body_survives_an_inventory_round_trip(tmp_path: Path):
    """Without serialising `empty_body`, a reloaded inventory puts every heading-only
    parent back into `expected` to be scored `missing`."""
    inventory = _empty_body_inventory("1.105")
    path = tmp_path / "inventory.json"
    path.write_text(render_official_inventory(inventory), encoding="utf-8")
    reloaded = load_official_inventory(path)
    before = {p.key.section: p.empty_body for p in inventory.provisions}
    after = {p.key.section: p.empty_body for p in reloaded.provisions}
    assert before == after and before["1.105"] is True

    baseline = build_baseline(
        inventory=reloaded,
        inventory_sha256=SHA_B,
        dataset=_evidence(),
        candidates=[
            _candidate(
                FederalCorpus.CFR, "1.106", "Contracting authority.", ordinal=1, title="48"
            )
        ],
    )
    counts = coverage_counts(baseline.entries)
    assert counts["expected"] == 2 and counts["empty_official_body"] == 1


def test_a_pre_stratum_inventory_is_rejected_rather_than_silently_defaulted(
    tmp_path: Path,
):
    """A schema-1 inventory has no `empty_body` field. Defaulting it to False would put
    1,469 CFR sections back into `expected` and report a 4x-overstated `missing` -- so the
    load must fail loudly instead."""
    inventory = _empty_body_inventory("1.105")
    payload = json.loads(render_official_inventory(inventory))
    payload["schema_version"] = 1
    for item in payload["provisions"]:
        del item["empty_body"]
    path = tmp_path / "old-inventory.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported official inventory schema"):
        load_official_inventory(path)


def test_ecfr_projection_marks_heading_only_parents_as_empty(tmp_path: Path):
    """End to end from real-shaped bytes: the parent carries a heading and nothing else,
    its hyphen-suffixed children carry the law."""
    source = tmp_path / "title-48.xml"
    source.write_text(
        """<ECFR TITLE="48"><DIV5 TYPE="PART" N="1">
        <DIV8 TYPE="SECTION" N="1.105"><HEAD>1.105   Issuance.</HEAD></DIV8>
        <DIV8 TYPE="SECTION" N="1.105-1"><HEAD>1.105-1   Publication.</HEAD>
        <P>The FAR is published in...</P></DIV8>
        <DIV8 TYPE="SECTION" N="1.105-2"><HEAD>1.105-2   Arrangement.</HEAD>
        <P>The FAR is divided into...</P></DIV8>
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
    assert by_section["1.105"].empty_body is True
    assert by_section["1.105"].reserved is False    # empty, but not a placeholder
    assert by_section["1.105-1"].empty_body is False
    assert by_section["1.105-2"].empty_body is False


@pytest.mark.parametrize(
    "body",
    [
        "[Reserved]",                          # 2 CFR 700.0
        "§ 1542.5   [Reserved]",               # 49 CFR 1542.5 (degenerate <HEAD>)
        "908.7115-908.7117   [Reserved]",      # 48 CFR, a range, no section sign
        "  [Reserved].  ",                     # surrounding whitespace, trailing period
    ],
)
def test_a_body_that_is_only_a_reserved_marker_counts_as_reserved(body: str):
    assert _ECFR_RESERVED_BODY_RE.fullmatch(body.strip()) is not None


@pytest.mark.parametrize(
    "body",
    [
        "(a) [Reserved] (b) The Administrator shall publish a notice.",
        "[Reserved] for future use by the Secretary.",
        "The requirements of paragraph (c) [Reserved] do not apply.",
        "See § 1000.3.",
        "No.",
        "Reserved parking is prohibited.",
    ],
)
def test_a_body_containing_a_reserved_subsection_is_still_law(body: str):
    """This pattern must FULL-match, never search: thousands of sections full of law
    contain a reserved *subsection*, and swallowing them would delete real provisions
    from the denominator."""
    assert _ECFR_RESERVED_BODY_RE.fullmatch(body.strip()) is None


def test_ecfr_projection_finds_a_reserved_marker_that_landed_in_the_body(tmp_path: Path):
    """49 CFR 1542.5 is `<HEAD>§ 1542.5</HEAD>` with the heading line pushed into the body.
    Reading only <HEAD> scored all 8 such sections `missing` -- reporting absent law where
    the official source says the opposite."""
    source = tmp_path / "title-49.xml"
    source.write_text(
        """<ECFR TITLE="49"><DIV5 TYPE="PART" N="1542">
        <DIV8 TYPE="SECTION" N="1542.5"><HEAD>§ 1542.5</HEAD>
        <P>§ 1542.5   [Reserved]</P></DIV8>
        <DIV8 TYPE="SECTION" N="1542.7"><HEAD>§ 1542.7 Inspections.</HEAD>
        <P>(a) [Reserved]</P><P>(b) Each airport operator must allow inspection.</P></DIV8>
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
    assert by_section["1542.5"].reserved is True
    # ... and a section that merely CONTAINS a reserved subsection keeps its law.
    assert by_section["1542.7"].reserved is False
    assert by_section["1542.7"].empty_body is False


def test_a_corpus_level_date_gap_is_not_per_provision_staleness():
    """Establishing the CFR cutoff at 2026-08-12 against a 2026-08-26 edition would have
    marked all 217,607 represented sections `stale`. Only 203 (0.09%) were actually
    amended in that window -- a ~1000x overstatement. Without a per-provision date the
    honest answer is that this provision's currency cannot be certified, so currency
    abstains and the skew is reported separately."""
    provision = _official(FederalCorpus.CFR, "1.1", "official text")
    baseline = build_baseline(
        _inventory(FederalCorpus.CFR, (provision,), cutoff="2026-08-26"),
        inventory_sha256=SHA_B,
        candidates=(_candidate(FederalCorpus.CFR, "1.1", "official text", ordinal=1),),
        dataset=_evidence(cutoff="2026-08-12"),
    )
    entry = baseline.entries[0]
    assert entry.currency_status == CurrencyStatus.PENDING
    assert entry.currency_status != CurrencyStatus.STALE
    counts = coverage_counts(baseline.entries)
    assert counts["stale"] == 0 and counts["pending_currency"] == 1


@pytest.mark.parametrize(
    ("amended", "dataset_cutoff", "expected"),
    [
        ("2026-08-20", "2026-08-12", CurrencyStatus.STALE),    # changed after the snapshot
        ("2026-08-12", "2026-08-12", CurrencyStatus.ALIGNED),  # changed on the boundary
        ("2026-01-05", "2026-08-12", CurrencyStatus.ALIGNED),  # long settled
    ],
)
def test_a_per_provision_amendment_date_decides_staleness(
    amended: str, dataset_cutoff: str, expected: CurrencyStatus
):
    """With the provision's own last official amendment, `stale` means what it says:
    this section changed after the snapshot was taken."""
    provision = replace(
        _official(FederalCorpus.CFR, "1.1", "official text"),
        official_amendment_date=amended,
    )
    entry = build_baseline(
        _inventory(FederalCorpus.CFR, (provision,), cutoff="2026-08-26"),
        inventory_sha256=SHA_B,
        candidates=(_candidate(FederalCorpus.CFR, "1.1", "official text", ordinal=1),),
        dataset=_evidence(cutoff=dataset_cutoff),
    ).entries[0]
    assert entry.currency_status == expected


def test_official_amendment_date_round_trips_and_must_be_a_date(tmp_path: Path):
    with pytest.raises(ValueError, match="official_amendment_date"):
        replace(_official(FederalCorpus.CFR, "1.1", "t"), official_amendment_date="Aug 2026")
    inventory = _inventory(
        FederalCorpus.CFR,
        (replace(_official(FederalCorpus.CFR, "1.1", "t"), official_amendment_date="2026-08-20"),
         _official(FederalCorpus.CFR, "1.2", "u")),
    )
    path = tmp_path / "inv.json"
    path.write_text(render_official_inventory(inventory), encoding="utf-8")
    reloaded = load_official_inventory(path)
    got = {p.key.section: p.official_amendment_date for p in reloaded.provisions}
    assert got == {"1.1": "2026-08-20", "1.2": None}
