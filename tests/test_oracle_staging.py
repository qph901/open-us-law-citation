"""Hermetic tests for the oracle stager (COV-1A).

A fake ``fetcher`` stands in for the official-government downloads, so no network or
staged bytes are needed. The invariant under test is verify-before-record: the
registry is pinned (``local_path``/``sha256`` set) only after every expected byte is
present and parseable, and never on a partial or malformed response.
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import pytest

import scripts.stage_oracle as st
from open_us_law_citation.oracle_manifest import load_oracle_manifest

_USLM_ID = "oracle:uslm:test:2025-01-06"
_ECFR_ID = "oracle:ecfr:test:2026-08-26"
_ECFR_TEMPLATE = "https://ecfr.example/api/full/2026-08-26/title-{title}.xml"


def _write_registry(path: Path) -> None:
    """A minimal, valid, fully *unstaged* two-edition registry."""
    raw = {
        "schema_version": 1,
        "snapshot": "v2026.08",
        "dataset_revision": "0" * 40,
        "repository_commit_date": "2026-08-26",
        "repository_commit_date_is_content_cutoff": False,
        "oracle_editions": [
            {
                "oracle_edition": _USLM_ID,
                "kind": "uslm",
                "edition_date": "2025-01-06",
                "source_url": "https://uscode.example/releasepoints/rp.htm",
                "local_path": None,
                "sha256": None,
            },
            {
                "oracle_edition": _ECFR_ID,
                "kind": "ecfr",
                "edition_date": "2026-08-26",
                "source_url": _ECFR_TEMPLATE,
                "local_path": None,
                "sha256": None,
            },
        ],
        "corpora": [
            {
                "corpus": "us_federal_statutes",
                "snapshot_content_cutoff": "2025-01-06",
                "cutoff_status": "established",
                "basis": "test",
                "comparison_oracle_edition": _USLM_ID,
                "residual_skew_days": 0,
            },
            {
                "corpus": "us_federal_regulations",
                "snapshot_content_cutoff": None,
                "cutoff_status": "unresolved",
                "basis": "test",
                "comparison_oracle_edition": _ECFR_ID,
                "residual_skew_days": None,
            },
        ],
    }
    path.write_text(json.dumps(raw, indent=2) + "\n")


def _ecfr_fetcher(bad_title: int | None = None):
    def fetch(url: str) -> bytes:
        title = url.rsplit("title-", 1)[1].split(".")[0]
        if bad_title is not None and title == str(bad_title):
            return b"<html><body>404 Not Found</body></html>"  # not a well-formed section doc
        return f"<ecfr><title number='{title}'/></ecfr>".encode()
    return fetch


def _zip_bytes(members: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    return buffer.getvalue()


# --- pure helpers ---------------------------------------------------------------


def test_parse_title_spec_range_and_list():
    assert st.parse_title_spec("1-3") == [1, 2, 3]
    assert st.parse_title_spec("1,2,5-7") == [1, 2, 5, 6, 7]
    assert st.parse_title_spec("3, 1 , 2") == [1, 2, 3]


def test_parse_title_spec_rejects_inverted_and_empty():
    with pytest.raises(ValueError):
        st.parse_title_spec("9-1")
    with pytest.raises(ValueError):
        st.parse_title_spec("")


def test_ecfr_title_url_substitution_and_guard():
    assert st.ecfr_title_url(_ECFR_TEMPLATE, 5).endswith("title-5.xml")
    with pytest.raises(ValueError):
        st.ecfr_title_url("https://ecfr.example/no-placeholder.xml", 5)


def test_require_valid_xml_rejects_empty_and_html():
    with pytest.raises(ValueError):
        st._require_valid_xml("t.xml", b"   ")
    with pytest.raises(ValueError):
        st._require_valid_xml("t.xml", b"<html><body>error</body></html><trailing")


# --- staging primitives ---------------------------------------------------------


def test_stage_ecfr_writes_every_title(tmp_path):
    out = tmp_path / "ecfr"
    staged = st.stage_ecfr(_ECFR_TEMPLATE, [1, 2, 3], out, _ecfr_fetcher())
    assert [p.name for p in staged] == ["title-1.xml", "title-2.xml", "title-3.xml"]
    assert all(p.exists() for p in staged)


def test_stage_ecfr_rejects_malformed_response(tmp_path):
    out = tmp_path / "ecfr"
    with pytest.raises(ValueError):
        st.stage_ecfr(_ECFR_TEMPLATE, [1, 2], out, _ecfr_fetcher(bad_title=2))


def test_stage_uslm_accepts_xml_and_zip(tmp_path):
    xml_out = tmp_path / "rp.xml"
    st.stage_uslm("https://x/rp.xml", xml_out, lambda u: b"<usc/>")
    assert xml_out.read_bytes() == b"<usc/>"

    zip_out = tmp_path / "rp.zip"
    payload = _zip_bytes({"usc01.xml": b"<usc/>"})
    st.stage_uslm("https://x/rp.zip", zip_out, lambda u: payload)
    assert zipfile.is_zipfile(zip_out)


def test_stage_uslm_rejects_html_and_empty_zip(tmp_path):
    with pytest.raises(ValueError):
        st.stage_uslm("https://x/rp.htm", tmp_path / "a", lambda u: b"<html></html>x")
    with pytest.raises(ValueError):
        st.stage_uslm("https://x/rp.zip", tmp_path / "b.zip",
                      lambda u: _zip_bytes({"readme.txt": b"no xml here"}))


# --- pin writer -----------------------------------------------------------------


def test_pin_edition_sets_both_fields_and_revalidates(tmp_path):
    reg = tmp_path / "reg.json"
    _write_registry(reg)
    st.pin_edition(reg, _USLM_ID, Path("data/oracles/rp.zip"), "a" * 64)
    manifest = load_oracle_manifest(reg)
    edition = next(e for e in manifest.editions if e.oracle_edition == _USLM_ID)
    assert edition.staged
    assert edition.local_path == "data/oracles/rp.zip"
    assert edition.sha256 == "a" * 64
    # Byte-stable shape: 2-space indent + trailing newline, still loads.
    assert reg.read_text().endswith("}\n")


def test_pin_edition_unknown_id_raises(tmp_path):
    reg = tmp_path / "reg.json"
    _write_registry(reg)
    with pytest.raises(SystemExit):
        st.pin_edition(reg, "oracle:nope", Path("x"), "a" * 64)


def test_pin_edition_rejects_bad_sha_and_leaves_file_intact(tmp_path):
    reg = tmp_path / "reg.json"
    _write_registry(reg)
    before = reg.read_text()
    with pytest.raises(Exception):
        st.pin_edition(reg, _USLM_ID, Path("x"), "not-a-sha")
    assert reg.read_text() == before  # atomic: original untouched on validation failure


# --- end to end -----------------------------------------------------------------


def test_stage_ecfr_end_to_end_pins_tree_hash(tmp_path):
    reg = tmp_path / "reg.json"
    _write_registry(reg)
    out = tmp_path / "data" / "ecfr"
    sha256, method = st.stage(reg, _ECFR_ID, out, titles=[1, 2, 3], fetcher=_ecfr_fetcher())
    assert method == "sha256_tree_v1"
    assert len(sha256) == 64
    edition = next(e for e in load_oracle_manifest(reg).editions
                   if e.oracle_edition == _ECFR_ID)
    assert edition.staged and edition.sha256 == sha256


def test_stage_uslm_end_to_end_pins_byte_hash(tmp_path):
    reg = tmp_path / "reg.json"
    _write_registry(reg)
    out = tmp_path / "data" / "rp.zip"
    payload = _zip_bytes({"usc01.xml": b"<usc/>"})
    sha256, method = st.stage(reg, _USLM_ID, out, url="https://x/rp.zip",
                              fetcher=lambda u: payload)
    assert method == "sha256_bytes_v1"
    edition = next(e for e in load_oracle_manifest(reg).editions
                   if e.oracle_edition == _USLM_ID)
    assert edition.staged and edition.sha256 == sha256


def test_stage_does_not_pin_on_partial_fetch(tmp_path):
    reg = tmp_path / "reg.json"
    _write_registry(reg)
    out = tmp_path / "data" / "ecfr"
    with pytest.raises(ValueError):
        st.stage(reg, _ECFR_ID, out, titles=[1, 2, 3], fetcher=_ecfr_fetcher(bad_title=3))
    # The registry must remain unstaged — a partial corpus is never certified.
    edition = next(e for e in load_oracle_manifest(reg).editions
                   if e.oracle_edition == _ECFR_ID)
    assert not edition.staged


def test_stage_refuses_already_pinned_without_overwrite(tmp_path):
    reg = tmp_path / "reg.json"
    _write_registry(reg)
    out = tmp_path / "data" / "ecfr"
    st.stage(reg, _ECFR_ID, out, titles=[1], fetcher=_ecfr_fetcher())
    with pytest.raises(SystemExit):
        st.stage(reg, _ECFR_ID, tmp_path / "data" / "ecfr2", titles=[1],
                 fetcher=_ecfr_fetcher())


def test_stage_refuses_existing_output_without_overwrite(tmp_path):
    reg = tmp_path / "reg.json"
    _write_registry(reg)
    out = tmp_path / "data" / "ecfr"
    out.mkdir(parents=True)
    with pytest.raises(SystemExit):
        st.stage(reg, _ECFR_ID, out, titles=[1], fetcher=_ecfr_fetcher())
