"""Reproduce the v2026.08 CFR text-mismatch experiment; never repair source data.

This is a snapshot-specific audit, not a production text normalizer. It compares
an exact repeated-span removal candidate with the existing official projection.
All candidate edits stay in memory; only measurements and source coordinates are
written. Conflicting removal spans abstain. No fuzzy comparison is used.

Run from the repository root with ``uv run python scripts/audit_text_mismatch.py``.
The temporary CFR-only DuckDB uses about 800 MB of disk, with a 1 GB engine memory
limit. Python retains one title's dataset bodies and one official section at a
time. Optional JSONL details contain hashes/coordinates, never legal-text bodies.
"""

from __future__ import annotations

import argparse
import json
import re
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import duckdb

from open_us_law_citation.coverage_baseline import (
    _ECFR_RESERVED_BODY_RE,
    _ECFR_RESERVED_RE,
    OFFICIAL_TEXT_PROJECTION,
    TEXT_NORMALIZATION,
    FederalCorpus,
    ProvisionKey,
    _direct_child,
    _flatten_xml_text_excluding,
    _validate_source_schema,
    normalize_legal_text,
    oracle_source_sha256,
    text_fingerprints,
)
from open_us_law_citation.source_record import compute_source_record_id, file_sha256

SNAPSHOT = "v2026.08"
DATASET_SHA256 = "6d9bcda025dc9eeeaa1361a8317369899cd87751e4eaa4095049518e611ad26e"
ORACLE_SHA256 = "1f8c4bf7ba7bfec19842e8a4b5959d794afc3b5384577c986639b80d22586ccd"
METHOD = "exact_newline_overlap_390_400_audit_v1"


def propose_removals(text: str) -> tuple[str, list[tuple[int, int, int]], bool]:
    """Find 390–400 identical characters on either side of a newline run.

    Each tuple is (removal_start, removal_end, repeated_character_count), using
    zero-based, half-open Python character offsets into the original raw text.
    Remove the newline run and the second copy. Keep all other bytes unchanged.
    Legitimate repeated text can satisfy this rule: agreement must be evaluated
    separately. Conflicting intervals return the original text without editing.
    """
    spans = []
    for match in re.finditer(r"\n+", text):
        start, end = match.span()
        for size in range(400, 389, -1):
            if start >= size and text[start - size:start] == text[end:end + size]:
                spans.append((start, end + size, size))
                break
    conflict = any(a[1] > b[0] for a, b in zip(spans, spans[1:]))
    if conflict:
        return text, spans, True
    pieces = []
    previous = 0
    for start, end, _ in spans:
        pieces.append(text[previous:start])
        previous = end
    pieces.append(text[previous:])
    return "".join(pieces), spans, False


def audit(root: Path, scratch: Path, details) -> dict:
    dataset = root / "data/v2026.08_full/us_federal_regulations.parquet"
    oracle = root / "data/oracles/ecfr-2026-08-26"
    if file_sha256(dataset) != DATASET_SHA256:
        raise ValueError("dataset bytes differ from the audited snapshot")
    if oracle_source_sha256(oracle) != (ORACLE_SHA256, "sha256_tree_v1"):
        raise ValueError("oracle bytes differ from the audited edition")
    _validate_source_schema(dataset)
    paths = sorted(oracle.glob("title-*.xml"), key=lambda p: int(p.stem.split("-")[-1]))
    if {p.stem for p in paths} != {f"title-{i}" for i in range(1, 51) if i != 35}:
        raise ValueError("expected all 49 non-reserved CFR titles")

    totals: Counter = Counter()
    lengths: Counter = Counter()
    signals: Counter = Counter()
    by_title = {}
    examples: dict[str, list] = defaultdict(list)
    con = duckdb.connect(
        str(scratch / "cfr.duckdb"), config={"memory_limit": "1GB", "threads": "2"}
    )
    try:
        con.execute(
            """CREATE TABLE cfr AS SELECT
               coalesce(title_number, regexp_extract(act_id, '^CFR_T([0-9]+)_', 1))
                   AS title,
               section_number, act_id, file_row_number AS ordinal, text
               FROM read_parquet(?, file_row_number=true)
               WHERE starts_with(act_id, 'CFR_')""",
            [str(dataset)],
        )
        for path in paths:
            title = path.stem.split("-")[-1]
            rows: dict[ProvisionKey, list] = defaultdict(list)
            for section, aid, ordinal, text in con.execute(
                "SELECT section_number, act_id, ordinal, text FROM cfr WHERE title=?",
                [title],
            ).fetchall():
                rows[ProvisionKey(FederalCorpus.CFR, title, section)].append(
                    (aid, ordinal, text)
                )
            counts: Counter = Counter()
            seen = set()
            for _, element in ET.iterparse(path, events=("end",)):
                if element.attrib.get("TYPE") != "SECTION":
                    continue
                key = ProvisionKey(FederalCorpus.CFR, title, element.attrib["N"])
                if key in seen:
                    raise ValueError(f"duplicate official key: {key.canonical_id}")
                seen.add(key)
                head = _direct_child(element, "head")
                heading = "".join(head.itertext()) if head is not None else ""
                official = _flatten_xml_text_excluding(element, head)
                expected = normalize_legal_text(official)
                counts["official"] += 1
                if _ECFR_RESERVED_RE.search(heading) or _ECFR_RESERVED_BODY_RE.fullmatch(
                    official.strip()
                ):
                    counts["reserved"] += 1
                elif not expected:
                    counts["empty"] += 1
                else:
                    counts["expected"] += 1
                    candidates = rows.get(key, [])
                    if len(candidates) != 1:
                        counts["multi" if candidates else "missing"] += 1
                    else:
                        aid, ordinal, text = candidates[0]
                        if text is None:
                            raise ValueError("unexpected null text in the pinned snapshot")
                        proposed, spans, conflict = propose_removals(text)
                        before = normalize_legal_text(text)
                        after = normalize_legal_text(proposed)
                        matched_before = before == expected
                        matched_after = after == expected
                        counts.update({
                            "represented": 1,
                            "exact": int(text == official),
                            "normalized": int(matched_before),
                            "mismatch": int(not matched_before),
                            "seam_detected": int(bool(spans)),
                            "conflicting_seams": int(conflict),
                            "post_normalized": int(matched_after),
                            "recovered": int(not matched_before and matched_after),
                            "regressed": int(matched_before and not matched_after),
                            "residual": int(not matched_after),
                        })
                        lengths.update(size for _, _, size in spans)
                        if not matched_before or spans:
                            outcome = (
                                "regressed" if matched_before and not matched_after
                                else "recovered" if matched_after else "residual"
                            )
                            item = {
                                "key": key.canonical_id,
                                "act_id": aid,
                                "ordinal": ordinal,
                                "source_record_id": compute_source_record_id(
                                    SNAPSHOT, DATASET_SHA256, ordinal
                                ),
                                "official_normalized_sha256": text_fingerprints(official)[1],
                                "raw_text_sha256": text_fingerprints(text)[0],
                                "candidate_text_sha256": text_fingerprints(proposed)[0],
                                "official_length": len(expected),
                                "raw_length": len(before),
                                "candidate_length": len(after),
                                "proposed_removals": spans,
                                "conflicting_seams": conflict,
                                "outcome": outcome,
                            }
                            if len(examples[outcome]) < 3:
                                examples[outcome].append(item)
                            if details is not None:
                                details.write(json.dumps(item, sort_keys=True) + "\n")
                        if not matched_after:
                            signals.update({
                                "lowercase_head": int(bool(re.match("[a-z]", text.lstrip()))),
                                "dataset_amendment_banner": int(
                                    "Link to an amendment published" in text
                                ),
                                "candidate_contained_in_official": int(after in expected),
                                "has_detected_seam": int(bool(spans)),
                                "conflicting_seams": int(conflict),
                            })
                element.clear()
            totals.update(counts)
            by_title[title] = dict(counts)
            print(f"Title {title}: {counts['recovered']} recovered; "
                  f"{counts['residual']} residual", flush=True)
    finally:
        con.close()
    baseline = {
        "official": 227521, "expected": 219056, "represented": 217607,
        "exact": 133218, "normalized": 154383, "mismatch": 63224,
        "reserved": 7001, "empty": 1464, "missing": 366, "multi": 1083,
    }
    if any(totals[key] != value for key, value in baseline.items()):
        raise ValueError("audit input counts do not reproduce the committed COV-1A baseline")
    return {
        "schema_version": 1,
        "method": METHOD,
        "snapshot": SNAPSHOT,
        "dataset_sha256": DATASET_SHA256,
        "oracle_edition": "oracle:ecfr:point-in-time:2026-08-26",
        "oracle_sha256": ORACLE_SHA256,
        "official_projection": OFFICIAL_TEXT_PROJECTION,
        "normalization": TEXT_NORMALIZATION,
        "totals": dict(totals),
        "by_title": by_title,
        "detected_overlap_lengths": dict(lengths),
        "residual_signals_nonexclusive": dict(signals),
        "examples": dict(examples),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path,
                        default=Path("reports/text_mismatch_experiment.json"))
    parser.add_argument("--details-output", type=Path)
    parser.add_argument("--scratch-dir", type=Path)
    args = parser.parse_args()
    details = None
    try:
        if args.details_output is not None:
            args.details_output.parent.mkdir(parents=True, exist_ok=True)
            details = args.details_output.open("w")
        with tempfile.TemporaryDirectory(prefix="oul-text-audit-", dir=args.scratch_dir) as tmp:
            result = audit(args.root, Path(tmp), details)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result["totals"], sort_keys=True))
    finally:
        if details is not None:
            details.close()


if __name__ == "__main__":
    main()
