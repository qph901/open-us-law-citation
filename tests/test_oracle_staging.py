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
    result = st.stage_ecfr(_ECFR_TEMPLATE, [1, 2, 3], out, _ecfr_fetcher())
    assert [p.name for p in result.staged] == ["title-1.xml", "title-2.xml", "title-3.xml"]
    assert result.reused == [] and result.missing == []
    assert all(p.exists() for p in result.staged)


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


def test_http_fetch_requests_and_decodes_gzip(monkeypatch):
    """The eCFR versioner API answers HTTP 406 to a request that does not permit
    compression ("This endpoint requires response compression"), and urllib neither
    offers nor decodes gzip by default -- so `http_fetch` must do both itself."""
    import gzip
    import urllib.request

    captured: dict[str, object] = {}

    class _FakeResponse:
        headers = {"Content-Encoding": "gzip"}

        def read(self):
            return gzip.compress(b"<ECFR>payload</ECFR>")

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def _fake_urlopen(request, timeout=None):
        captured["headers"] = {k.casefold(): v for k, v in request.header_items()}
        return _FakeResponse()

    monkeypatch.setattr(urllib.request, "urlopen", _fake_urlopen)
    body = st.http_fetch("https://www.ecfr.gov/api/versioner/v1/full/2026-08-26/title-3.xml")

    assert "gzip" in str(captured["headers"].get("accept-encoding", "")).casefold()
    assert body == b"<ECFR>payload</ECFR>"   # decompressed, not raw gzip


def test_http_fetch_passes_through_an_uncompressed_response(monkeypatch):
    """A server that ignores the header and answers uncompressed must still work."""
    import urllib.request

    class _PlainResponse:
        headers: dict[str, str] = {}

        def read(self):
            return b"<ECFR>plain</ECFR>"

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: _PlainResponse())
    assert st.http_fetch("https://www.ecfr.gov/x.xml") == b"<ECFR>plain</ECFR>"


def _fetcher_with(missing: set[int] | None = None, fail_times: dict[int, int] | None = None):
    """A fake eCFR fetcher: `missing` titles 404, `fail_times` titles fail N times first."""
    missing = missing or set()
    remaining = dict(fail_times or {})

    def fetch(url: str) -> bytes:
        title = int(url.rsplit("title-", 1)[1].split(".")[0])
        if title in missing:
            raise st.ResourceNotFound(f"{url}: HTTP 404")
        if remaining.get(title, 0) > 0:
            remaining[title] -= 1
            raise ConnectionResetError("reset mid-transfer")
        return f"<ecfr><title number='{title}'/></ecfr>".encode()

    return fetch


def test_an_unexpected_404_aborts_rather_than_shrinking_the_oracle(tmp_path):
    """Silently omitting a title would understate the coverage denominator with nothing
    in the record saying so."""
    with pytest.raises(SystemExit, match="no document"):
        st.stage_ecfr(_ECFR_TEMPLATE, [1, 2, 3], tmp_path / "e", _fetcher_with(missing={2}))


def test_a_title_reserved_in_its_entirety_may_be_declared_missing(tmp_path):
    """CFR title 35 is reserved in its entirety and has no full-text XML: HTTP 404 is the
    correct answer, so it is accepted when named -- and reported, never hidden."""
    result = st.stage_ecfr(
        _ECFR_TEMPLATE, [1, 35, 36], tmp_path / "e",
        _fetcher_with(missing={35}), allow_missing_titles={35},
    )
    assert result.missing == [35]
    assert [p.name for p in result.staged] == ["title-1.xml", "title-36.xml"]


def test_resume_keeps_valid_files_and_refetches_the_rest(tmp_path):
    out = tmp_path / "e"
    out.mkdir()
    (out / "title-1.xml").write_bytes(b"<ecfr><title number='1'/></ecfr>")
    (out / "title-2.xml").write_bytes(b"<html><body>truncated error page</body></html>")

    result = st.stage_ecfr(_ECFR_TEMPLATE, [1, 2, 3], out, _fetcher_with(), resume=True)
    assert result.reused == [1]                      # valid, kept without refetching
    assert 2 not in result.reused                    # the HTML page is refetched, not trusted
    assert len(result.staged) == 3
    assert b"<ecfr>" in (out / "title-2.xml").read_bytes()


def test_http_fetch_retries_a_transient_failure_then_succeeds(monkeypatch):
    import urllib.request

    attempts = {"n": 0}

    class _Resp:
        headers: dict[str, str] = {}

        def read(self):
            return b"<ECFR>ok</ECFR>"

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def _urlopen(request, timeout=None):
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ConnectionResetError("reset mid-transfer")
        return _Resp()

    monkeypatch.setattr(urllib.request, "urlopen", _urlopen)
    body = st.http_fetch("https://www.ecfr.gov/x.xml", sleep=lambda _s: None)
    assert body == b"<ECFR>ok</ECFR>" and attempts["n"] == 3


def test_http_fetch_never_retries_a_404(monkeypatch):
    """A 404 is permanent; retrying it wastes minutes across ~49 titles."""
    import urllib.error
    import urllib.request

    attempts = {"n": 0}

    def _urlopen(request, timeout=None):
        attempts["n"] += 1
        raise urllib.error.HTTPError("https://x", 404, "Not Found", {}, None)

    monkeypatch.setattr(urllib.request, "urlopen", _urlopen)
    with pytest.raises(st.ResourceNotFound):
        st.http_fetch("https://www.ecfr.gov/x.xml", sleep=lambda _s: None)
    assert attempts["n"] == 1


def test_http_fetch_gives_up_after_max_attempts(monkeypatch):
    import urllib.request

    attempts = {"n": 0}

    def _urlopen(request, timeout=None):
        attempts["n"] += 1
        raise ConnectionResetError("reset")

    monkeypatch.setattr(urllib.request, "urlopen", _urlopen)
    with pytest.raises(RuntimeError, match="giving up after 3"):
        st.http_fetch("https://www.ecfr.gov/x.xml", max_attempts=3, sleep=lambda _s: None)
    assert attempts["n"] == 3


def test_resume_refuses_a_directory_this_tool_did_not_leave_midrun(tmp_path):
    """The tree hash certifies whatever is in the directory, so resuming into an
    unmarked one could pin bytes of unknown provenance under this edition's id."""
    reg = tmp_path / "oracles.json"
    _write_registry(reg)
    out = tmp_path / "data" / "ecfr"
    out.mkdir(parents=True)
    (out / "title-1.xml").write_bytes(b"<ecfr><title number='1'/></ecfr>")
    with pytest.raises(SystemExit, match="no staging marker"):
        st.stage(reg, _ECFR_ID, out, titles=[1, 2], fetcher=_ecfr_fetcher(), resume=True)


def test_resume_refuses_when_the_marker_is_for_another_edition(tmp_path):
    reg = tmp_path / "oracles.json"
    _write_registry(reg)
    out = tmp_path / "data" / "ecfr"
    out.mkdir(parents=True)
    st.staging_marker(out).write_text(
        json.dumps({"oracle_edition": "oracle:ecfr:some-other:2020-01-01",
                    "source_url": _ECFR_TEMPLATE})
    )
    with pytest.raises(SystemExit, match="Refusing to certify another edition"):
        st.stage(reg, _ECFR_ID, out, titles=[1], fetcher=_ecfr_fetcher(), resume=True)


def test_marker_lives_outside_the_tree_and_is_cleared_on_success(tmp_path):
    """It must not be inside the staged directory: sha256_tree_v1 would hash it, so the
    pin would certify the resume bookkeeping as part of the oracle."""
    reg = tmp_path / "oracles.json"
    _write_registry(reg)
    out = tmp_path / "data" / "ecfr"
    sha256, method = st.stage(reg, _ECFR_ID, out, titles=[1, 2, 3], fetcher=_ecfr_fetcher())
    assert method == "sha256_tree_v1"
    assert st.staging_marker(out).parent == out.parent   # sibling, not child
    assert not st.staging_marker(out).exists()           # cleared once pinned
    assert sorted(p.name for p in out.iterdir()) == [
        "title-1.xml", "title-2.xml", "title-3.xml",
    ]


def test_an_interrupted_run_leaves_a_marker_that_lets_resume_finish_it(tmp_path):
    reg = tmp_path / "oracles.json"
    _write_registry(reg)
    out = tmp_path / "data" / "ecfr"
    # Title 2 fails hard the first time, so the run aborts after staging title 1.
    with pytest.raises(RuntimeError):
        st.stage(reg, _ECFR_ID, out, titles=[1, 2, 3],
                 fetcher=_raising_fetcher_after(1), overwrite=False)
    assert st.staging_marker(out).exists()               # resume state survives
    assert (out / "title-1.xml").exists()

    sha256, _ = st.stage(reg, _ECFR_ID, out, titles=[1, 2, 3],
                         fetcher=_ecfr_fetcher(), resume=True)
    assert len(sha256) == 64
    assert not st.staging_marker(out).exists()


def _raising_fetcher_after(last_good: int):
    def fetch(url: str) -> bytes:
        title = int(url.rsplit("title-", 1)[1].split(".")[0])
        if title > last_good:
            raise RuntimeError("network died mid-run")
        return f"<ecfr><title number='{title}'/></ecfr>".encode()

    return fetch
