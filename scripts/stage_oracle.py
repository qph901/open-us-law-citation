"""Stage and checksum-pin an official oracle edition into the registry.

COV-1A separates a *selected* oracle (a URL + date in ``oracles/<snapshot>.json``
with ``local_path``/``sha256`` still null) from a *pinned* one. A pin exists only
after the **complete** official bytes have been fetched, verified, and hashed —
never from an unverified URL, a partial transfer, or a moving ``current`` response
(see ``DATA.md``). This tool performs that staging with the same verify-before-record
discipline as :mod:`scripts.download`: it writes ``local_path``/``sha256`` back into
the registry **only** after every expected byte is present and parseable.

Two edition kinds, matching the two hashing methods in
:func:`open_us_law_citation.coverage_baseline.oracle_source_sha256`:

* **USLM** (USC): a single official artifact (the release-point ``.zip`` of per-title
  USLM XML, or one XML file) → ``sha256_bytes_v1``. The registry ``source_url`` is the
  release-point ``.htm`` index, so point ``--url`` at the actual bulk ZIP.
* **eCFR** (CFR): a directory of unmodified point-in-time versioner XML responses, one
  per title, fetched from the ``…/full/<date>/title-{title}.xml`` template →
  ``sha256_tree_v1``.

The operator runs this (it performs the official-government downloads); a fake
``fetcher`` makes the logic hermetically testable.

    uv run python scripts/stage_oracle.py \
        --oracle-manifest oracles/v2026.08.json \
        --edition oracle:ecfr:point-in-time:2026-08-26 \
        --out data/oracles/ecfr-2026-08-26 --titles 1-50 --allow-missing 35

``--allow-missing 35`` is required at the 2026-08-26 edition: CFR title 35 is reserved in
its entirety and the versioner returns HTTP 404 for it. An *unlisted* 404 aborts the run,
so a title cannot go missing from the oracle without someone saying so. If the run is
interrupted (large titles take minutes), re-run the same command with ``--resume``: title
files already on disk are re-validated and kept, and the rest are refetched.

    uv run python scripts/stage_oracle.py \
        --oracle-manifest oracles/v2026.08.json \
        --edition oracle:uslm:usc-pl-118-274-not-118-159:2025-01-06 \
        --out data/oracles/uslm-usc-118-274not159.zip \
        --url https://uscode.house.gov/download/releasepoints/us/pl/118/274not159/usc-rp@118-274not159.zip
"""

from __future__ import annotations

import argparse
import gzip
import json
import shutil
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree as ET

from open_us_law_citation.coverage_baseline import oracle_source_sha256
from open_us_law_citation.oracle_manifest import OracleKind, load_oracle_manifest

# A fetcher maps an https URL to its raw response bytes. The default hits the
# network; tests inject a fake so no official download is required.
Fetcher = Callable[[str], bytes]

_USER_AGENT = "open-us-law-citation/COV-1A oracle-stager"


class ResourceNotFound(Exception):
    """The source has no document at this URL (HTTP 404).

    Distinct from a transient failure: it is never retried, and it is the one outcome a
    caller may legitimately treat as expected — a CFR title reserved in its entirety has
    no full-text XML at all (title 35 at the 2026-08-26 edition returns 404).
    """


# Retry only what can plausibly succeed on a second attempt. A 404 is permanent; a 5xx,
# a 429, or a dropped connection is not. Large titles take minutes -- title 40 is roughly
# 6x title 21 -- and a mid-transfer reset was observed against the live API, so a staging
# run of ~49 titles without retry is unlikely to complete.
_RETRY_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})
_MAX_ATTEMPTS = 4
_BACKOFF_SECONDS = 5.0


def http_fetch(
    url: str,
    *,
    timeout: float = 600.0,
    max_attempts: int = _MAX_ATTEMPTS,
    sleep: Callable[[float], None] = time.sleep,
) -> bytes:
    """Fetch one https URL to bytes. https-only, matching the registry invariant.

    ``Accept-Encoding: gzip`` is **required**, not an optimisation: the eCFR versioner API
    answers a request without it with ``HTTP 406`` and the body ``"This endpoint requires
    response compression. Send an Accept-Encoding header that permits compression."``
    (reproduced against the live API on 2026-09-08). urllib neither offers compression nor
    decodes it by default, so both halves are done here.
    """
    if not url.startswith("https://"):
        raise ValueError(f"refusing to fetch non-https URL: {url!r}")
    request = urllib.request.Request(
        url, headers={"User-Agent": _USER_AGENT, "Accept-Encoding": "gzip"}
    )
    last: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
                payload = response.read()
                encoding = (response.headers.get("Content-Encoding") or "").strip().casefold()
            if encoding == "gzip":
                payload = gzip.decompress(payload)
            return payload
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise ResourceNotFound(f"{url}: HTTP 404") from exc
            if exc.code not in _RETRY_STATUSES:
                raise
            last = exc
        except (urllib.error.URLError, TimeoutError, ConnectionError, gzip.BadGzipFile) as exc:
            # A reset or truncated body yields a partial payload we must NOT keep.
            last = exc
        if attempt < max_attempts:
            sleep(_BACKOFF_SECONDS * (2 ** (attempt - 1)))
    raise RuntimeError(f"{url}: giving up after {max_attempts} attempts ({last})") from last


def parse_title_spec(spec: str) -> list[int]:
    """Parse a title spec like ``1-50`` or ``1,2,5-9`` into a sorted unique list."""
    titles: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            low_s, high_s = part.split("-", 1)
            low, high = int(low_s), int(high_s)
            if low > high:
                raise ValueError(f"inverted title range: {part!r}")
            titles.update(range(low, high + 1))
        else:
            titles.add(int(part))
    if not titles:
        raise ValueError("no titles selected")
    return sorted(titles)


def _require_valid_xml(name: str, data: bytes) -> None:
    """Reject an empty body or an HTML error page masquerading as the source XML."""
    if not data.strip():
        raise ValueError(f"{name}: empty response — refusing to stage a zero-byte oracle")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        head = data[:80].decode("utf-8", "replace")
        raise ValueError(f"{name}: response is not well-formed XML ({exc}); starts {head!r}")
    # A common failure is a well-formed *HTML* error page (200-with-body, or a
    # soft 404). Legal source XML never has an <html> root, so reject it rather than
    # certify an error page as the oracle.
    if root.tag.rsplit("}", 1)[-1].casefold() == "html":
        raise ValueError(f"{name}: response is an HTML document, not source XML")


def ecfr_title_url(template: str, title: int) -> str:
    """Substitute a title number into the versioner ``…/title-{title}.xml`` template."""
    if "{title}" not in template:
        raise ValueError("eCFR source_url must contain a '{title}' placeholder")
    return template.replace("{title}", str(title))


def staging_marker(out_dir: Path) -> Path:
    """Resume state, kept **beside** the staged tree, never inside it.

    ``sha256_tree_v1`` hashes every file under the directory, so a marker within it would
    change what the pin certifies. It lives as a sibling dotfile and is removed on success.
    """
    return out_dir.parent / f".{out_dir.name}.staging-state.json"


def _resumable(path: Path) -> bool:
    """Is an already-present title file usable as-is? Re-validated, never trusted."""
    if not path.is_file():
        return False
    try:
        _require_valid_xml(path.name, path.read_bytes())
    except (ValueError, OSError):
        return False
    return True


@dataclass(frozen=True)
class EcfrStaging:
    staged: list[Path]
    reused: list[int]     # titles already on disk and revalidated (resume)
    missing: list[int]    # titles the source has no document for (HTTP 404)


def stage_ecfr(
    template: str,
    titles: list[int],
    out_dir: Path,
    fetcher: Fetcher,
    *,
    allow_missing_titles: frozenset[int] | set[int] = frozenset(),
    resume: bool = False,
) -> EcfrStaging:
    """Fetch every requested title's point-in-time XML into ``out_dir``.

    Each response is validated as well-formed XML before it is written, so a partial
    corpus or an error page can never reach the hash step.

    A title the source has no document for (HTTP 404) is a legitimate outcome — a CFR
    title reserved in its entirety has no full-text XML — but it is only *accepted* when
    named in ``allow_missing_titles``. An unexpected 404 aborts, because silently omitting
    a title would shrink the oracle and understate the coverage denominator without
    anything in the record saying so.

    With ``resume``, a title already on disk that still parses is kept and not refetched.
    The file is re-validated rather than trusted; the caller is responsible for ensuring
    the directory belongs to this edition (see :func:`staging_marker`).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    staged: list[Path] = []
    reused: list[int] = []
    missing: list[int] = []
    for title in titles:
        name = f"title-{title}.xml"
        path = out_dir / name
        if resume and _resumable(path):
            staged.append(path)
            reused.append(title)
            continue
        try:
            data = fetcher(ecfr_title_url(template, title))
        except ResourceNotFound:
            if title not in allow_missing_titles:
                raise SystemExit(
                    f"title {title}: source has no document (HTTP 404). If this title is "
                    f"reserved in its entirety, re-run with --allow-missing {title}; "
                    f"otherwise the oracle would be silently short a title."
                )
            missing.append(title)
            continue
        _require_valid_xml(name, data)
        path.write_bytes(data)
        staged.append(path)
    if not staged:
        raise ValueError("eCFR staging produced no titles")
    return EcfrStaging(staged=staged, reused=reused, missing=missing)


def stage_uslm(url: str, out_path: Path, fetcher: Fetcher) -> Path:
    """Fetch a single USLM artifact (release ZIP or one XML) to ``out_path``.

    Validates the payload is a ZIP or well-formed XML — not the ``.htm`` release-point
    index or an error page — before it can be hashed.
    """
    data = fetcher(url)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    if zipfile.is_zipfile(out_path):
        with zipfile.ZipFile(out_path) as archive:
            if not any(n.casefold().endswith(".xml") for n in archive.namelist()):
                raise ValueError(f"{out_path.name}: ZIP contains no XML members")
        return out_path
    _require_valid_xml(out_path.name, data)
    return out_path


def pin_edition(
    manifest_path: Path,
    edition_id: str,
    local_path: Path,
    sha256: str,
) -> None:
    """Write ``local_path`` + ``sha256`` into the registry edition, byte-stably.

    Loads the raw JSON, sets exactly the two fields on the matching edition, and
    re-validates the whole registry through :func:`load_oracle_manifest` (so the
    both-set-or-both-null invariant and sha format are enforced) before overwriting
    the file with 2-space indentation and a trailing newline.
    """
    raw = json.loads(manifest_path.read_text())
    editions = raw.get("oracle_editions", [])
    matches = [e for e in editions if e.get("oracle_edition") == edition_id]
    if not matches:
        raise SystemExit(f"edition {edition_id!r} not found in {manifest_path}")
    if len(matches) > 1:
        raise SystemExit(f"edition {edition_id!r} is not unique in {manifest_path}")
    matches[0]["local_path"] = local_path.as_posix()
    matches[0]["sha256"] = sha256
    serialized = json.dumps(raw, indent=2) + "\n"
    # Round-trip through the validated loader before touching the file on disk.
    tmp = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    tmp.write_text(serialized)
    try:
        load_oracle_manifest(tmp)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
    tmp.replace(manifest_path)


def stage(
    manifest_path: Path,
    edition_id: str,
    out: Path,
    *,
    titles: list[int] | None = None,
    url: str | None = None,
    fetcher: Fetcher = http_fetch,
    overwrite: bool = False,
    allow_missing_titles: frozenset[int] | set[int] = frozenset(),
    resume: bool = False,
) -> tuple[str, str]:
    """Stage one edition end to end and pin it. Returns ``(sha256, method)``.

    Refuses to overwrite an already-pinned edition or an existing output path unless
    ``overwrite`` is set — a re-run must be a deliberate act, never a silent reshuffle
    of what a checksum certifies.
    """
    manifest = load_oracle_manifest(manifest_path)
    edition = next((e for e in manifest.editions if e.oracle_edition == edition_id), None)
    if edition is None:
        raise SystemExit(f"edition {edition_id!r} not found in {manifest_path}")
    if edition.staged and not overwrite:
        raise SystemExit(
            f"edition {edition_id!r} is already pinned (local_path/sha256 set). "
            f"Pass --overwrite to re-stage."
        )
    if resume and edition.kind != OracleKind.ECFR:
        raise SystemExit("--resume applies to eCFR staging only (USLM is a single file)")
    if out.exists() and not resume:
        if not overwrite:
            raise SystemExit(
                f"output {out} already exists. Pass --overwrite to replace, or --resume "
                f"to continue an interrupted run."
            )
        if out.is_dir():
            shutil.rmtree(out)
        else:
            out.unlink()

    if edition.kind == OracleKind.ECFR:
        if not titles:
            raise SystemExit("eCFR staging requires --titles (e.g. 1-50)")
        template = url or edition.source_url
        # The tree hash certifies whatever is in the directory, so resuming into a
        # directory left by a DIFFERENT edition (or a different source template) would pin
        # foreign bytes under this edition's id. The marker makes that unrepresentable:
        # it records what the interrupted run was staging, and resume refuses on mismatch.
        marker = staging_marker(out)
        expected = {"oracle_edition": edition_id, "source_url": template}
        if resume:
            if not marker.exists():
                raise SystemExit(
                    f"--resume: no staging marker at {marker}. Refusing to resume into a "
                    f"directory this tool did not leave mid-run; re-stage with --overwrite."
                )
            found = json.loads(marker.read_text())
            if {k: found.get(k) for k in expected} != expected:
                raise SystemExit(
                    f"--resume: {marker} was written for {found.get('oracle_edition')!r} "
                    f"from {found.get('source_url')!r}, not {edition_id!r}. Refusing to "
                    f"certify another edition's bytes under this one."
                )
        else:
            out.mkdir(parents=True, exist_ok=True)
            marker.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        result = stage_ecfr(
            template, titles, out, fetcher,
            allow_missing_titles=allow_missing_titles, resume=resume,
        )
        if result.missing:
            print(f"titles with no document at this edition (allowed): {result.missing}")
        if result.reused:
            print(f"titles reused from the interrupted run: {len(result.reused)}")
    else:  # USLM
        source = url or edition.source_url
        stage_uslm(source, out, fetcher)

    sha256, method = oracle_source_sha256(out)
    pin_edition(manifest_path, edition_id, out, sha256)
    # Pinned: the run is complete, so the resume state is no longer meaningful.
    if edition.kind == OracleKind.ECFR:
        staging_marker(out).unlink(missing_ok=True)
    return sha256, method


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--oracle-manifest", type=Path, required=True)
    ap.add_argument("--edition", required=True, help="oracle_edition id to stage")
    ap.add_argument("--out", type=Path, required=True,
                    help="output directory (eCFR) or file (USLM), under gitignored data/")
    ap.add_argument("--titles", default=None,
                    help="eCFR only: title spec, e.g. '1-50' or '1,2,5-9'")
    ap.add_argument("--url", default=None,
                    help="override the fetch URL (e.g. the USLM release ZIP; the "
                         "registry source_url is the .htm index)")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--resume", action="store_true",
                    help="eCFR only: continue an interrupted run, keeping title files "
                         "already on disk that still validate.")
    ap.add_argument("--allow-missing", default=None,
                    help="eCFR only: title spec the source legitimately has no document "
                         "for (e.g. '35', a title reserved in its entirety). An "
                         "unlisted 404 aborts.")
    args = ap.parse_args(argv)
    titles = parse_title_spec(args.titles) if args.titles else None
    allow_missing = (
        frozenset(parse_title_spec(args.allow_missing)) if args.allow_missing else frozenset()
    )
    sha256, method = stage(
        args.oracle_manifest, args.edition, args.out,
        titles=titles, url=args.url, overwrite=args.overwrite,
        allow_missing_titles=allow_missing, resume=args.resume,
    )
    print(f"pinned {args.edition}", flush=True)
    print(f"  local_path: {args.out.as_posix()}", flush=True)
    print(f"  sha256:     {sha256}  ({method})", flush=True)


if __name__ == "__main__":
    main()
