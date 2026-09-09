"""COV-1A: deterministic official-denominator federal coverage baselines.

This module deliberately separates three questions that are easy to blur:

* structural crosswalk -- does an official ``(title, section)`` key map to zero,
  one, or multiple Open US Law rows?
* currency -- is the dataset's established legal-content cutoff aligned with the
  official title cutoff, older (``stale``), or still unknown?
* text agreement -- do comparable single provisions agree exactly or after a
  conservative whitespace normalization?

An official inventory is always the denominator.  Dataset row/file counts are
never accepted as one.  USC mismatches remain pending until anatomy can separate
operative text from editorial material; multi-row CFR matches remain pending
until CFR assembly has decided whether the rows compose.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

from .oracle_manifest import CutoffStatus, OracleKind, load_oracle_manifest
from .source_record import CanonicalSourceRecord, file_sha256, iter_source_records

SCHEMA_VERSION = 1
MATCH_METHOD = "canonical_title_section_v1"
TEXT_NORMALIZATION = "unicode_nfc_whitespace_v1"
OFFICIAL_TEXT_PROJECTION = "xml_text_nodes_newline_v1"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SECTION_MARK_RE = re.compile(r"^\s*\N{SECTION SIGN}{1,2}\s*")
_USLM_TITLE_RE = re.compile(r"(?:^|[^a-z])usc(?:ode)?[-_ ]*0*(\d+)", re.I)
_ECFR_TITLE_RE = re.compile(r"title[-_ ]*0*(\d+)", re.I)
# eCFR marks a reserved section ONLY in its <HEAD> ("§ 1.8   [Reserved]"). There is no
# RESERVED attribute in the full-title XML -- verified against titles 1, 3, 11 and 23 at
# the 2026-08-26 edition, where every one of the 64 [Reserved] sections is an element with
# an empty body. The trailing-period variant ("[Reserved].") is real and must match: it is
# the one case where the eCFR structure API's own `reserved` flag disagrees, and the XML is
# right -- 23 CFR 1270.5 is an empty placeholder that the API reports as not reserved.
_ECFR_RESERVED_RE = re.compile(r"\[\s*reserved\s*\]", re.I)


class FederalCorpus(StrEnum):
    USC = "usc"
    CFR = "cfr"


class StructuralStatus(StrEnum):
    REPRESENTED = "represented"
    MISSING = "missing"
    # A section the official source publishes as an empty placeholder (`[Reserved]`).
    # It is neither present law nor absent law, so it is its own stratum and is held out
    # of the coverage denominator entirely -- scoring it `missing` would invent a gap.
    RESERVED = "reserved"
    DUPLICATE = "duplicate"
    AMBIGUOUS = "ambiguous"
    UNEXPECTED = "unexpected"


class CurrencyStatus(StrEnum):
    ALIGNED = "aligned"
    STALE = "stale"
    AHEAD_OF_ORACLE = "ahead_of_oracle"
    PENDING = "pending"
    NOT_APPLICABLE = "not_applicable"


class TextAgreement(StrEnum):
    EXACT = "exact"
    NORMALIZED_ONLY = "normalized_only"
    MISMATCH = "mismatch"
    PENDING_USC_ANATOMY = "pending_usc_anatomy"
    PENDING_CFR_ASSEMBLY = "pending_cfr_assembly"
    UNAVAILABLE = "unavailable"


def _iso_date(value: str, field: str) -> str:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an ISO date, got {value!r}") from exc
    return value


def _require_sha256(value: str, field: str) -> str:
    if not _SHA256_RE.fullmatch(value):
        raise ValueError(f"{field} must be 64 lowercase hexadecimal characters")
    return value


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_legal_text(text: str) -> str:
    """Conservative comparison normalization; it does not alter punctuation/case."""
    return " ".join(unicodedata.normalize("NFC", text).split())


def text_fingerprints(text: str | None) -> tuple[str | None, str | None]:
    if text is None:
        return None, None
    return _content_hash(text), _content_hash(normalize_legal_text(text))


def _canonical_section(value: str) -> str:
    section = unicodedata.normalize("NFKC", value).replace("\u00a0", " ")
    section = _SECTION_MARK_RE.sub("", section)
    section = " ".join(section.strip().split()).casefold()
    if not section:
        raise ValueError("section must be non-empty")
    return section


@dataclass(frozen=True, slots=True)
class ProvisionKey:
    corpus: FederalCorpus
    title: str
    section: str

    def __post_init__(self) -> None:
        if not isinstance(self.corpus, FederalCorpus):
            raise ValueError(f"corpus must be a FederalCorpus, got {self.corpus!r}")
        try:
            title_number = int(self.title)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"title must be a positive integer, got {self.title!r}") from exc
        if title_number <= 0:
            raise ValueError(f"title must be a positive integer, got {self.title!r}")
        object.__setattr__(self, "title", str(title_number))
        object.__setattr__(self, "section", _canonical_section(self.section))

    @property
    def canonical_id(self) -> str:
        return f"us:{self.corpus}:{self.title}:{self.section}"


@dataclass(frozen=True, slots=True)
class TitleCurrency:
    title: str
    legal_content_cutoff: str
    basis: str

    def __post_init__(self) -> None:
        try:
            title = int(self.title)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"title must be a positive integer, got {self.title!r}") from exc
        if title <= 0 or not self.basis:
            raise ValueError("title must be positive and basis must be non-empty")
        object.__setattr__(self, "title", str(title))
        _iso_date(self.legal_content_cutoff, "legal_content_cutoff")


@dataclass(frozen=True, slots=True)
class OfficialProvision:
    key: ProvisionKey
    official_id: str
    source_url: str
    raw_text_sha256: str | None
    normalized_text_sha256: str | None
    # eCFR publishes reserved sections as empty `[Reserved]` placeholders, frequently over a
    # *range* of numbers in a single element (`N="102.104-102.109"`), so a reserved key is
    # often not a section number that could ever match a dataset row. See `_ECFR_RESERVED_RE`.
    reserved: bool = False

    def __post_init__(self) -> None:
        if not self.official_id:
            raise ValueError("official_id must be non-empty")
        if urlparse(self.source_url).scheme != "https":
            raise ValueError("official provision source_url must use https")
        for field in ("raw_text_sha256", "normalized_text_sha256"):
            value = getattr(self, field)
            if value is not None:
                _require_sha256(value, field)
        if (self.raw_text_sha256 is None) != (self.normalized_text_sha256 is None):
            raise ValueError("official raw and normalized text hashes must both be set or null")

    @classmethod
    def from_text(
        cls,
        *,
        key: ProvisionKey,
        official_id: str,
        source_url: str,
        text: str | None,
        reserved: bool = False,
    ) -> OfficialProvision:
        raw_hash, normalized_hash = text_fingerprints(text)
        return cls(key, official_id, source_url, raw_hash, normalized_hash, reserved)


@dataclass(frozen=True, slots=True)
class DatasetCandidate:
    key: ProvisionKey
    source_record_id: str
    act_id: str
    source_url: str | None
    raw_text_sha256: str | None
    normalized_text_sha256: str | None

    def __post_init__(self) -> None:
        if not self.source_record_id or not self.act_id:
            raise ValueError("source_record_id and act_id must be non-empty")
        for field in ("raw_text_sha256", "normalized_text_sha256"):
            value = getattr(self, field)
            if value is not None:
                _require_sha256(value, field)
        if (self.raw_text_sha256 is None) != (self.normalized_text_sha256 is None):
            raise ValueError("candidate raw and normalized text hashes must both be set or null")

    @classmethod
    def from_source_record(
        cls, record: CanonicalSourceRecord, corpus: FederalCorpus
    ) -> DatasetCandidate:
        title = record.column("title_number")
        section = record.column("section_number")
        act_id = record.column("act_id")
        if title is None or section is None or act_id is None:
            raise ValueError(
                f"{record.source_record_id}: federal candidate lacks title/section/act_id"
            )
        raw_hash, normalized_hash = text_fingerprints(record.raw_text)
        return cls(
            key=ProvisionKey(corpus, title, section),
            source_record_id=record.source_record_id,
            act_id=act_id,
            source_url=record.column("source_url"),
            raw_text_sha256=raw_hash,
            normalized_text_sha256=normalized_hash,
        )


@dataclass(frozen=True, slots=True)
class OfficialInventory:
    corpus: FederalCorpus
    oracle_edition: str
    oracle_kind: OracleKind
    edition_date: str
    source_url: str
    source_sha256: str
    title_currency: tuple[TitleCurrency, ...]
    provisions: tuple[OfficialProvision, ...]
    source_hash_method: str = "sha256_bytes_v1"

    def __post_init__(self) -> None:
        if not isinstance(self.corpus, FederalCorpus):
            raise ValueError("corpus must be a FederalCorpus")
        if not isinstance(self.oracle_kind, OracleKind):
            raise ValueError("oracle_kind must be an OracleKind")
        if not isinstance(self.title_currency, tuple) or not isinstance(
            self.provisions, tuple
        ):
            raise ValueError("title_currency and provisions must be immutable tuples")
        if not self.oracle_edition.startswith("oracle:"):
            raise ValueError("oracle_edition must be a stable 'oracle:' identifier")
        expected_kind = OracleKind.USLM if self.corpus == FederalCorpus.USC else OracleKind.ECFR
        if self.oracle_kind != expected_kind:
            raise ValueError(f"{self.corpus} inventories require oracle kind {expected_kind}")
        _iso_date(self.edition_date, "edition_date")
        if urlparse(self.source_url).scheme != "https":
            raise ValueError("official inventory source_url must use https")
        _require_sha256(self.source_sha256, "source_sha256")
        if self.source_hash_method not in ("sha256_bytes_v1", "sha256_tree_v1"):
            raise ValueError("unsupported official source_hash_method")

        currencies = {item.title: item for item in self.title_currency}
        if len(currencies) != len(self.title_currency):
            raise ValueError("title_currency contains duplicate titles")
        if not self.provisions:
            raise ValueError("official inventory must contain at least one provision")
        seen: set[ProvisionKey] = set()
        for provision in self.provisions:
            if provision.key.corpus != self.corpus:
                raise ValueError("official provision corpus differs from inventory corpus")
            if provision.key.title not in currencies:
                raise ValueError(
                    f"official title {provision.key.title} lacks title-level currency"
                )
            if provision.key in seen:
                raise ValueError(f"duplicate official provision key {provision.key.canonical_id}")
            seen.add(provision.key)

    def currency_by_title(self) -> dict[str, TitleCurrency]:
        return {item.title: item for item in self.title_currency}


@dataclass(frozen=True, slots=True)
class DatasetEvidence:
    snapshot: str
    dataset_revision: str
    source_file: str
    source_file_sha256: str
    legal_content_cutoff: str | None
    cutoff_status: CutoffStatus
    excluded_federal_register_rows: int = 0
    excluded_other_rows: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.cutoff_status, CutoffStatus):
            raise ValueError("cutoff_status must be a CutoffStatus")
        if not self.snapshot or not self.dataset_revision or not self.source_file:
            raise ValueError("snapshot, dataset_revision, and source_file must be non-empty")
        _require_sha256(self.source_file_sha256, "source_file_sha256")
        if self.legal_content_cutoff is not None:
            _iso_date(self.legal_content_cutoff, "legal_content_cutoff")
        if (self.cutoff_status == CutoffStatus.ESTABLISHED) != (
            self.legal_content_cutoff is not None
        ):
            raise ValueError("established dataset cutoffs require a date")
        if self.excluded_federal_register_rows < 0 or self.excluded_other_rows < 0:
            raise ValueError("excluded row counts cannot be negative")


@dataclass(frozen=True, slots=True)
class CrosswalkEntry:
    key: ProvisionKey
    official: OfficialProvision | None
    candidates: tuple[DatasetCandidate, ...]
    structural_status: StructuralStatus
    currency_status: CurrencyStatus
    text_agreement: TextAgreement

    @property
    def is_discrepancy(self) -> bool:
        return (
            self.structural_status != StructuralStatus.REPRESENTED
            or self.currency_status != CurrencyStatus.ALIGNED
            or self.text_agreement
            not in (TextAgreement.EXACT, TextAgreement.NORMALIZED_ONLY)
        )


@dataclass(frozen=True, slots=True)
class CoverageBaseline:
    inventory: OfficialInventory
    inventory_sha256: str
    dataset: DatasetEvidence
    entries: tuple[CrosswalkEntry, ...]

    def __post_init__(self) -> None:
        _require_sha256(self.inventory_sha256, "inventory_sha256")
        if not isinstance(self.entries, tuple):
            raise ValueError("entries must be an immutable tuple")


def _entry_sort_key(key: ProvisionKey) -> tuple[int, tuple[tuple[int, Any], ...], str]:
    pieces: list[tuple[int, Any]] = []
    for part in re.split(r"(\d+)", key.section):
        pieces.append((0, int(part)) if part.isdigit() else (1, part))
    return int(key.title), tuple(pieces), key.section


def _structural_status(
    official: OfficialProvision | None, candidates: Sequence[DatasetCandidate]
) -> StructuralStatus:
    if official is None:
        return StructuralStatus.UNEXPECTED
    if official.reserved:
        # Reserved regardless of whether the snapshot happens to carry a row for the key:
        # the official source publishes no law here, so there is nothing to be missing.
        return StructuralStatus.RESERVED
    if not candidates:
        return StructuralStatus.MISSING
    if len(candidates) == 1:
        return StructuralStatus.REPRESENTED
    raw_hashes = {candidate.raw_text_sha256 for candidate in candidates}
    if None not in raw_hashes and len(raw_hashes) == 1:
        return StructuralStatus.DUPLICATE
    return StructuralStatus.AMBIGUOUS


def _currency_status(
    official: OfficialProvision | None,
    candidates: Sequence[DatasetCandidate],
    *,
    dataset_cutoff: str | None,
    official_cutoff: str | None,
) -> CurrencyStatus:
    if official is None or not candidates:
        return CurrencyStatus.NOT_APPLICABLE
    if dataset_cutoff is None or official_cutoff is None:
        return CurrencyStatus.PENDING
    if dataset_cutoff == official_cutoff:
        return CurrencyStatus.ALIGNED
    if dataset_cutoff < official_cutoff:
        return CurrencyStatus.STALE
    return CurrencyStatus.AHEAD_OF_ORACLE


def _text_agreement(
    corpus: FederalCorpus,
    official: OfficialProvision | None,
    candidates: Sequence[DatasetCandidate],
) -> TextAgreement:
    if official is None or not candidates:
        return TextAgreement.UNAVAILABLE
    if len(candidates) != 1:
        if corpus == FederalCorpus.CFR:
            return TextAgreement.PENDING_CFR_ASSEMBLY
        return TextAgreement.PENDING_USC_ANATOMY
    candidate = candidates[0]
    if official.raw_text_sha256 is None or candidate.raw_text_sha256 is None:
        return TextAgreement.UNAVAILABLE
    if official.raw_text_sha256 == candidate.raw_text_sha256:
        return TextAgreement.EXACT
    if official.normalized_text_sha256 == candidate.normalized_text_sha256:
        return TextAgreement.NORMALIZED_ONLY
    if corpus == FederalCorpus.USC:
        return TextAgreement.PENDING_USC_ANATOMY
    return TextAgreement.MISMATCH


def build_baseline(
    inventory: OfficialInventory,
    *,
    inventory_sha256: str,
    candidates: Iterable[DatasetCandidate],
    dataset: DatasetEvidence,
) -> CoverageBaseline:
    """Build the deterministic zero/one/multiple provision crosswalk."""
    _require_sha256(inventory_sha256, "inventory_sha256")
    official_by_key = {provision.key: provision for provision in inventory.provisions}
    candidate_by_key: defaultdict[ProvisionKey, list[DatasetCandidate]] = defaultdict(list)
    for candidate in candidates:
        if candidate.key.corpus != inventory.corpus:
            raise ValueError("dataset candidate corpus differs from official inventory")
        candidate_by_key[candidate.key].append(candidate)

    currency_by_title = inventory.currency_by_title()
    entries: list[CrosswalkEntry] = []
    for key in sorted(set(official_by_key) | set(candidate_by_key), key=_entry_sort_key):
        official = official_by_key.get(key)
        grouped = tuple(
            sorted(
                candidate_by_key.get(key, ()),
                key=lambda item: (item.source_record_id, item.act_id),
            )
        )
        official_cutoff = (
            currency_by_title[key.title].legal_content_cutoff
            if official is not None
            else None
        )
        entries.append(
            CrosswalkEntry(
                key=key,
                official=official,
                candidates=grouped,
                structural_status=_structural_status(official, grouped),
                currency_status=_currency_status(
                    official,
                    grouped,
                    dataset_cutoff=dataset.legal_content_cutoff,
                    official_cutoff=official_cutoff,
                ),
                text_agreement=_text_agreement(inventory.corpus, official, grouped),
            )
        )
    return CoverageBaseline(inventory, inventory_sha256, dataset, tuple(entries))


def _empty_counts() -> dict[str, int]:
    return {
        "expected": 0,
        "represented": 0,
        "missing": 0,
        "reserved": 0,
        "stale": 0,
        "duplicate": 0,
        "ambiguous": 0,
        "unexpected": 0,
        "exact_text": 0,
        "normalized_text": 0,
        "normalized_only_text": 0,
        "mismatch_text": 0,
        "pending_text": 0,
        "unavailable_text": 0,
        "aligned_currency": 0,
        "ahead_of_oracle_currency": 0,
        "pending_currency": 0,
        "not_applicable_currency": 0,
    }


def _add_entry(counts: dict[str, int], entry: CrosswalkEntry) -> None:
    # `expected` is the coverage DENOMINATOR, so it counts official sections that carry
    # law: reserved placeholders are excluded and tallied in their own `reserved` bucket
    # (via structural_status below). Including them would understate coverage by ~3.1% of
    # the CFR -- 6,985 of 227,521 sections at the 2026-08-26 edition.
    reserved = entry.official is not None and entry.official.reserved
    if entry.official is not None and not reserved:
        counts["expected"] += 1
    counts[entry.structural_status.value] += 1
    if entry.currency_status == CurrencyStatus.STALE:
        counts["stale"] += 1
    elif entry.currency_status == CurrencyStatus.ALIGNED:
        counts["aligned_currency"] += 1
    elif entry.currency_status == CurrencyStatus.AHEAD_OF_ORACLE:
        counts["ahead_of_oracle_currency"] += 1
    elif entry.currency_status == CurrencyStatus.PENDING:
        counts["pending_currency"] += 1
    else:
        counts["not_applicable_currency"] += 1
    if entry.official is None or reserved:
        # A reserved section has no operative text, so it enters no text-agreement bucket.
        return
    if entry.text_agreement == TextAgreement.EXACT:
        counts["exact_text"] += 1
        counts["normalized_text"] += 1
    elif entry.text_agreement == TextAgreement.NORMALIZED_ONLY:
        counts["normalized_text"] += 1
        counts["normalized_only_text"] += 1
    elif entry.text_agreement == TextAgreement.MISMATCH:
        counts["mismatch_text"] += 1
    elif entry.text_agreement in (
        TextAgreement.PENDING_USC_ANATOMY,
        TextAgreement.PENDING_CFR_ASSEMBLY,
    ):
        counts["pending_text"] += 1
    else:
        counts["unavailable_text"] += 1


def coverage_counts(entries: Iterable[CrosswalkEntry]) -> dict[str, int]:
    counts = _empty_counts()
    for entry in entries:
        _add_entry(counts, entry)
    return counts


def coverage_rates(counts: Mapping[str, int]) -> dict[str, str | None]:
    """Official-denominator percentages as fixed, byte-stable decimal strings."""
    denominator = counts["expected"]

    def percentage(name: str) -> str | None:
        if denominator == 0:
            return None
        value = Decimal(counts[name]) * Decimal(100) / Decimal(denominator)
        return format(value.quantize(Decimal("0.0001")), "f")

    return {
        "represented_percent": percentage("represented"),
        "missing_percent": percentage("missing"),
        "stale_percent": percentage("stale"),
        "duplicate_percent": percentage("duplicate"),
        "ambiguous_percent": percentage("ambiguous"),
        "exact_text_percent": percentage("exact_text"),
        "normalized_text_percent": percentage("normalized_text"),
        "mismatch_text_percent": percentage("mismatch_text"),
        "pending_text_percent": percentage("pending_text"),
    }


def _entry_dict(entry: CrosswalkEntry) -> dict[str, Any]:
    return {
        "provision_key": entry.key.canonical_id,
        "title": entry.key.title,
        "section": entry.key.section,
        "structural_status": entry.structural_status.value,
        "currency_status": entry.currency_status.value,
        "text_agreement": entry.text_agreement.value,
        "official_id": entry.official.official_id if entry.official else None,
        "official_source_url": entry.official.source_url if entry.official else None,
        "candidate_count": len(entry.candidates),
        "candidate_source_record_ids": [item.source_record_id for item in entry.candidates],
        "candidate_act_ids": [item.act_id for item in entry.candidates],
    }


def baseline_manifest(baseline: CoverageBaseline) -> dict[str, Any]:
    by_title: defaultdict[str, list[CrosswalkEntry]] = defaultdict(list)
    for entry in baseline.entries:
        by_title[entry.key.title].append(entry)
    currencies = baseline.inventory.currency_by_title()
    title_rows = []
    for title in sorted(by_title, key=int):
        title_counts = coverage_counts(by_title[title])
        title_rows.append(
            {
                "title": title,
                "official_legal_content_cutoff": (
                    currencies[title].legal_content_cutoff if title in currencies else None
                ),
                "official_currency_basis": (
                    currencies[title].basis if title in currencies else None
                ),
                "counts": title_counts,
                "rates": coverage_rates(title_counts),
            }
        )
    totals = coverage_counts(baseline.entries)
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact": "cov-1a-provision-coverage-baseline",
        "status": "preliminary",
        "jurisdiction": "US",
        "corpus": baseline.inventory.corpus.value,
        "snapshot": baseline.dataset.snapshot,
        "legal_content_cutoff": baseline.dataset.legal_content_cutoff,
        "cutoff_status": baseline.dataset.cutoff_status.value,
        "matching": {
            "method": MATCH_METHOD,
            "key": ["jurisdiction", "corpus", "title", "section"],
            "text_normalization": TEXT_NORMALIZATION,
            "official_text_projection": OFFICIAL_TEXT_PROJECTION,
            "represented_definition": "exactly one dataset candidate for an official key",
            "federal_register_in_cfr_denominator": False,
        },
        "oracle": {
            "oracle_edition": baseline.inventory.oracle_edition,
            "kind": baseline.inventory.oracle_kind.value,
            "edition_date": baseline.inventory.edition_date,
            "source_url": baseline.inventory.source_url,
            "source_sha256": baseline.inventory.source_sha256,
            "source_hash_method": baseline.inventory.source_hash_method,
            "inventory_sha256": baseline.inventory_sha256,
        },
        "dataset": {
            "source_file": baseline.dataset.source_file,
            "source_file_sha256": baseline.dataset.source_file_sha256,
            "dataset_revision": baseline.dataset.dataset_revision,
            "excluded_federal_register_rows": (
                baseline.dataset.excluded_federal_register_rows
            ),
            "excluded_other_rows": baseline.dataset.excluded_other_rows,
        },
        "totals": totals,
        "rates": coverage_rates(totals),
        "titles": title_rows,
        "discrepancies": [
            _entry_dict(entry) for entry in baseline.entries if entry.is_discrepancy
        ],
    }


def render_manifest_json(baseline: CoverageBaseline) -> str:
    return json.dumps(
        baseline_manifest(baseline), ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"


def render_markdown(baseline: CoverageBaseline, *, example_limit: int = 12) -> str:
    manifest = baseline_manifest(baseline)
    totals = manifest["totals"]
    rates = manifest["rates"]
    lines = [
        f"# COV-1A {baseline.inventory.corpus.upper()} provision coverage baseline",
        "",
        "**Status:** preliminary. This is an official-denominator structural/text "
        "baseline, not the COV-1B citation-resolution coverage gate.",
        "",
        "## Provenance",
        "",
        "- Jurisdiction: `US`",
        f"- Corpus: `{baseline.inventory.corpus}`",
        f"- Open US Law snapshot: `{baseline.dataset.snapshot}`",
        f"- Open US Law dataset revision: `{baseline.dataset.dataset_revision}`",
        f"- Dataset legal-content cutoff: "
        f"`{baseline.dataset.legal_content_cutoff or 'pending'}` "
        f"(`{baseline.dataset.cutoff_status}`)",
        f"- Official oracle: `{baseline.inventory.oracle_edition}`",
        f"- Oracle edition date: `{baseline.inventory.edition_date}`",
        f"- Oracle source: `{baseline.inventory.source_url}`",
        f"- Oracle source SHA-256: `{baseline.inventory.source_sha256}`",
        f"- Oracle source hash method: `{baseline.inventory.source_hash_method}`",
        f"- Normalized inventory SHA-256: `{baseline.inventory_sha256}`",
        f"- Dataset file: `{baseline.dataset.source_file}`",
        f"- Dataset file SHA-256: `{baseline.dataset.source_file_sha256}`",
        f"- Crosswalk: `{MATCH_METHOD}` over `(US, corpus, title, section)`",
        "- Federal Register rows in CFR denominator: **no**",
        "",
        "`represented` means exactly one dataset candidate at the official key. "
        "Currency and text agreement are separate dimensions; therefore a "
        "structurally represented provision can still be stale or text-pending.",
        "",
        "`reserved` is a **separate stratum held out of `expected`**, so every rate below "
        "is against sections that carry law. A reserved section is an empty official "
        "placeholder, not absent law, and eCFR often publishes one element over a whole "
        "*range* of numbers (`102.104-102.109`), which is not a key any dataset row could "
        "match -- scoring those `missing` would manufacture a coverage gap that does not "
        "exist.",
        "",
        "## Totals",
        "",
        "| expected | represented | missing | reserved | stale | duplicate | ambiguous | "
        "unexpected | exact text | normalized text | mismatch | pending text |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        f"| {totals['expected']:,} | {totals['represented']:,} | "
        f"{totals['missing']:,} | {totals['reserved']:,} | {totals['stale']:,} | "
        f"{totals['duplicate']:,} | {totals['ambiguous']:,} | "
        f"{totals['unexpected']:,} | {totals['exact_text']:,} | "
        f"{totals['normalized_text']:,} | {totals['mismatch_text']:,} | "
        f"{totals['pending_text']:,} |",
        "",
        "Official-denominator rates: "
        f"**structurally represented {rates['represented_percent']}%**, "
        f"missing {rates['missing_percent']}%, duplicate {rates['duplicate_percent']}%, "
        f"ambiguous {rates['ambiguous_percent']}%, stale {rates['stale_percent']}%, "
        f"exact text {rates['exact_text_percent']}%, and normalized text "
        f"{rates['normalized_text_percent']}%.",
        "",
        "Reserved official sections held out of the denominator (empty `[Reserved]` "
        f"placeholders): **{totals['reserved']:,}**.",
        "",
        "Currency overlays: "
        f"aligned `{totals['aligned_currency']:,}`, stale `{totals['stale']:,}`, "
        f"ahead of oracle `{totals['ahead_of_oracle_currency']:,}`, pending "
        f"`{totals['pending_currency']:,}`, not applicable "
        f"`{totals['not_applicable_currency']:,}`.",
        "",
        "## By title",
        "",
        "| title | official cutoff | expected | represented | represented % | missing | "
        "reserved | stale | "
        "duplicate | ambiguous | unexpected | exact | normalized | mismatch | pending |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for title in manifest["titles"]:
        counts = title["counts"]
        lines.append(
            f"| {title['title']} | {title['official_legal_content_cutoff'] or 'pending'} | "
            f"{counts['expected']:,} | {counts['represented']:,} | "
            f"{title['rates']['represented_percent'] or 'n/a'} | "
            f"{counts['missing']:,} | {counts['reserved']:,} | {counts['stale']:,} | "
            f"{counts['duplicate']:,} | {counts['ambiguous']:,} | "
            f"{counts['unexpected']:,} | {counts['exact_text']:,} | "
            f"{counts['normalized_text']:,} | {counts['mismatch_text']:,} | "
            f"{counts['pending_text']:,} |"
        )

    discrepancies = manifest["discrepancies"][:example_limit]
    lines.extend(["", "## Deterministic discrepancy sample", ""])
    if not discrepancies:
        lines.append("No discrepancies in this baseline.")
    else:
        lines.extend(
            [
                "| provision | structural | currency | text | candidates |",
                "|---|---|---|---|---:|",
            ]
        )
        for entry in discrepancies:
            lines.append(
                f"| `{entry['provision_key']}` | {entry['structural_status']} | "
                f"{entry['currency_status']} | {entry['text_agreement']} | "
                f"{entry['candidate_count']} |"
            )

    missing_examples = [
        entry
        for entry in manifest["discrepancies"]
        if entry["structural_status"] == StructuralStatus.MISSING
    ][:example_limit]
    unexpected_examples = [
        entry
        for entry in manifest["discrepancies"]
        if entry["structural_status"] == StructuralStatus.UNEXPECTED
    ][:example_limit]
    lines.extend(["", "## Unmatched official examples", ""])
    lines.extend(
        [f"- `{entry['provision_key']}` ({entry['official_id']})" for entry in missing_examples]
        or ["None."]
    )
    lines.extend(["", "## Dataset-only examples", ""])
    lines.extend(
        [
            f"- `{entry['provision_key']}` "
            f"({', '.join(entry['candidate_act_ids'])})"
            for entry in unexpected_examples
        ]
        or ["None."]
    )
    if baseline.dataset.excluded_federal_register_rows:
        lines.extend(
            [
                "",
                "## Federal Register separation",
                "",
                f"Excluded `{baseline.dataset.excluded_federal_register_rows:,}` "
                "Federal Register rows from the codified-CFR denominator. They are "
                "promulgation-record inventory and require a separate report.",
            ]
        )
    return "\n".join(lines) + "\n"


def official_inventory_dict(inventory: OfficialInventory) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact": "official-provision-inventory",
        "corpus": inventory.corpus.value,
        "oracle_edition": inventory.oracle_edition,
        "oracle_kind": inventory.oracle_kind.value,
        "edition_date": inventory.edition_date,
        "source_url": inventory.source_url,
        "source_sha256": inventory.source_sha256,
        "source_hash_method": inventory.source_hash_method,
        "official_text_projection": OFFICIAL_TEXT_PROJECTION,
        "title_currency": [
            {
                "title": item.title,
                "legal_content_cutoff": item.legal_content_cutoff,
                "basis": item.basis,
            }
            for item in sorted(inventory.title_currency, key=lambda item: int(item.title))
        ],
        "provisions": [
            {
                "title": provision.key.title,
                "section": provision.key.section,
                "official_id": provision.official_id,
                "source_url": provision.source_url,
                "raw_text_sha256": provision.raw_text_sha256,
                "normalized_text_sha256": provision.normalized_text_sha256,
            }
            for provision in sorted(
                inventory.provisions, key=lambda item: _entry_sort_key(item.key)
            )
        ],
    }


def render_official_inventory(inventory: OfficialInventory) -> str:
    return json.dumps(
        official_inventory_dict(inventory),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def load_official_inventory(path: str | Path) -> OfficialInventory:
    raw: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported official inventory schema {raw.get('schema_version')!r}")
    if raw.get("artifact") != "official-provision-inventory":
        raise ValueError("input is not an official-provision-inventory artifact")
    if raw.get("official_text_projection") != OFFICIAL_TEXT_PROJECTION:
        raise ValueError("official inventory uses an unsupported text projection")
    corpus = FederalCorpus(raw["corpus"])
    currencies = tuple(
        TitleCurrency(item["title"], item["legal_content_cutoff"], item["basis"])
        for item in raw["title_currency"]
    )
    provisions = tuple(
        OfficialProvision(
            key=ProvisionKey(corpus, item["title"], item["section"]),
            official_id=item["official_id"],
            source_url=item["source_url"],
            raw_text_sha256=item["raw_text_sha256"],
            normalized_text_sha256=item["normalized_text_sha256"],
        )
        for item in raw["provisions"]
    )
    return OfficialInventory(
        corpus=corpus,
        oracle_edition=raw["oracle_edition"],
        oracle_kind=OracleKind(raw["oracle_kind"]),
        edition_date=raw["edition_date"],
        source_url=raw["source_url"],
        source_sha256=raw["source_sha256"],
        title_currency=currencies,
        provisions=provisions,
        source_hash_method=raw.get("source_hash_method", "sha256_bytes_v1"),
    )


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].casefold()


def _flatten_xml_text(element: ET.Element) -> str:
    # Ignore indentation-only XML nodes but preserve boundaries between semantic
    # text nodes.  The exact metric is exact relative to this versioned projection.
    return "\n".join(part.strip() for part in element.itertext() if part.strip())


def _direct_child(element: ET.Element, name: str) -> ET.Element | None:
    return next((child for child in element if _local_name(child.tag) == name), None)


def _title_from_name(name: str, corpus: FederalCorpus) -> str | None:
    pattern = _USLM_TITLE_RE if corpus == FederalCorpus.USC else _ECFR_TITLE_RE
    match = pattern.search(Path(name).stem)
    return str(int(match.group(1))) if match else None


def _xml_documents(path: Path) -> Iterator[tuple[str, bytes]]:
    if path.is_dir():
        for item in sorted(path.rglob("*.xml")):
            yield item.as_posix(), item.read_bytes()
        return
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for name in sorted(archive.namelist()):
                if name.casefold().endswith(".xml") and not name.endswith("/"):
                    yield name, archive.read(name)
        return
    yield path.name, path.read_bytes()


def oracle_source_sha256(path: str | Path) -> tuple[str, str]:
    """Hash one official file or a directory of unmodified official XML files.

    A directory digest binds each sorted relative path and its byte hash. This
    lets a multi-title eCFR edition remain as the original HTTP response files;
    it need not be repackaged merely to obtain one edition provenance address.
    """
    source = Path(path)
    if source.is_file():
        return file_sha256(source), "sha256_bytes_v1"
    if not source.is_dir():
        raise ValueError("official source path must be an XML/ZIP file or directory")
    files = sorted(item for item in source.rglob("*.xml") if item.is_file())
    if not files:
        raise ValueError("official source directory contains no XML files")
    digest = hashlib.sha256()
    for item in files:
        relative = item.relative_to(source).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\x00")
        digest.update(bytes.fromhex(file_sha256(item)))
        digest.update(b"\x00")
    return digest.hexdigest(), "sha256_tree_v1"


def _uslm_provisions(
    name: str, data: bytes, source_url: str
) -> Iterator[OfficialProvision]:
    root = ET.fromstring(data)
    title = _title_from_name(name, FederalCorpus.USC)
    if title is None:
        for element in root.iter():
            if _local_name(element.tag) in ("docnumber", "docnum"):
                match = re.search(r"\b(\d+)\b", "".join(element.itertext()))
                if match:
                    title = str(int(match.group(1)))
                    break
    if title is None:
        raise ValueError(f"cannot determine USC title from {name!r}")

    for element in root.iter():
        if _local_name(element.tag) != "section":
            continue
        number = _direct_child(element, "num")
        if number is None:
            continue
        section = number.attrib.get("value") or "".join(number.itertext())
        if not section.strip():
            continue
        official_id = element.attrib.get("id") or f"usc-title-{title}-section-{section}"
        yield OfficialProvision.from_text(
            key=ProvisionKey(FederalCorpus.USC, title, section),
            official_id=official_id,
            source_url=source_url,
            text=_flatten_xml_text(element),
        )


def _ecfr_provisions(
    name: str, data: bytes, source_url: str
) -> Iterator[OfficialProvision]:
    root = ET.fromstring(data)
    title = _title_from_name(name, FederalCorpus.CFR)
    if title is None:
        root_title = root.attrib.get("TITLE") or root.attrib.get("title")
        if root_title and str(root_title).isdigit():
            title = str(int(root_title))
    if title is None:
        raise ValueError(f"cannot determine CFR title from {name!r}")

    for element in root.iter():
        if element.attrib.get("TYPE", "").casefold() != "section":
            continue
        head = _direct_child(element, "head")
        head_text = "".join(head.itertext()) if head is not None else ""
        reserved = bool(_ECFR_RESERVED_RE.search(head_text))
        section = element.attrib.get("N") or element.attrib.get("n")
        if not section:
            section = head_text
        match = re.search(r"\N{SECTION SIGN}{1,2}\s*([^\s—–]+)", section)
        if match:
            section = match.group(1)
        if not section.strip():
            continue
        official_id = element.attrib.get("ID") or element.attrib.get("id")
        official_id = official_id or f"cfr-title-{title}-section-{section}"
        yield OfficialProvision.from_text(
            key=ProvisionKey(FederalCorpus.CFR, title, section),
            official_id=official_id,
            source_url=source_url.format(title=title),
            text=_flatten_xml_text(element),
            reserved=reserved,
        )


def inventory_from_xml(
    *,
    source_path: str | Path,
    corpus: FederalCorpus,
    oracle_edition: str,
    oracle_kind: OracleKind,
    edition_date: str,
    source_url: str,
    source_sha256: str,
    currency_basis: str,
    title_cutoffs: Mapping[str, str] | None = None,
) -> OfficialInventory:
    """Project official XML into a deterministic, hash-only provision inventory."""
    path = Path(source_path)
    observed_source_sha256, source_hash_method = oracle_source_sha256(path)
    if observed_source_sha256 != source_sha256:
        raise ValueError("official source checksum differs from the pinned manifest")
    parser = _uslm_provisions if corpus == FederalCorpus.USC else _ecfr_provisions
    provisions: list[OfficialProvision] = []
    for name, data in _xml_documents(path):
        provisions.extend(parser(name, data, source_url))
    if not provisions:
        raise ValueError("official source produced zero section provisions")
    titles = sorted({item.key.title for item in provisions}, key=int)
    overrides = {str(int(key)): value for key, value in (title_cutoffs or {}).items()}
    unknown = set(overrides) - set(titles)
    if unknown:
        raise ValueError(f"title cutoff overrides reference absent titles: {sorted(unknown)}")
    currencies = tuple(
        TitleCurrency(
            title,
            overrides.get(title, edition_date),
            currency_basis,
        )
        for title in titles
    )
    return OfficialInventory(
        corpus=corpus,
        oracle_edition=oracle_edition,
        oracle_kind=oracle_kind,
        edition_date=edition_date,
        source_url=source_url,
        source_sha256=source_sha256,
        title_currency=currencies,
        provisions=tuple(provisions),
        source_hash_method=source_hash_method,
    )


def scan_dataset_candidates(
    path: str | Path,
    *,
    snapshot: str,
    dataset_revision: str,
    corpus: FederalCorpus,
    expected_sha256: str | None = None,
    legal_content_cutoff: str | None,
    cutoff_status: CutoffStatus,
) -> tuple[tuple[DatasetCandidate, ...], DatasetEvidence]:
    """Stream one federal Parquet and retain only compact provision fingerprints."""
    candidates: list[DatasetCandidate] = []
    excluded_fr = 0
    excluded_other = 0
    checksum: str | None = None
    for record in iter_source_records(path, snapshot, verify_checksum=expected_sha256):
        checksum = record.source_file_checksum
        act_id = record.column("act_id") or ""
        if corpus == FederalCorpus.CFR and act_id.startswith("FR_"):
            excluded_fr += 1
            continue
        wanted_prefix = "USC_" if corpus == FederalCorpus.USC else "CFR_"
        if not act_id.startswith(wanted_prefix):
            excluded_other += 1
            continue
        candidates.append(DatasetCandidate.from_source_record(record, corpus))
    checksum = checksum or file_sha256(path)
    evidence = DatasetEvidence(
        snapshot=snapshot,
        dataset_revision=dataset_revision,
        source_file=Path(path).name,
        source_file_sha256=checksum,
        legal_content_cutoff=legal_content_cutoff,
        cutoff_status=cutoff_status,
        excluded_federal_register_rows=excluded_fr,
        excluded_other_rows=excluded_other,
    )
    return tuple(candidates), evidence


def _manifest_selection(
    manifest_path: str | Path, corpus: FederalCorpus
) -> tuple[Any, Any, Any]:
    manifest = load_oracle_manifest(manifest_path)
    corpus_name = (
        "us_federal_statutes" if corpus == FederalCorpus.USC else "us_federal_regulations"
    )
    currency = next((item for item in manifest.corpora if item.corpus == corpus_name), None)
    if currency is None:
        raise ValueError(f"oracle manifest has no {corpus_name} currency record")
    edition = next(
        (
            item
            for item in manifest.editions
            if item.oracle_edition == currency.comparison_oracle_edition
        ),
        None,
    )
    if edition is None:
        raise ValueError(f"oracle manifest has no edition {currency.comparison_oracle_edition}")
    return manifest, edition, currency


def _build_inventory_command(args: argparse.Namespace) -> None:
    corpus = FederalCorpus(args.corpus)
    _, edition, _ = _manifest_selection(args.oracle_manifest, corpus)
    if not edition.staged or edition.local_path is None or edition.sha256 is None:
        raise SystemExit(
            f"{edition.oracle_edition} is not staged: set local_path and sha256 in "
            f"{args.oracle_manifest} only after the complete official bytes are present"
        )
    overrides: dict[str, str] = {}
    if args.title_cutoffs:
        overrides = json.loads(Path(args.title_cutoffs).read_text(encoding="utf-8"))
    inventory = inventory_from_xml(
        source_path=edition.local_path,
        corpus=corpus,
        oracle_edition=edition.oracle_edition,
        oracle_kind=edition.kind,
        edition_date=edition.edition_date,
        source_url=edition.source_url,
        source_sha256=edition.sha256,
        currency_basis=args.currency_basis,
        title_cutoffs=overrides,
    )
    Path(args.output).write_bytes(render_official_inventory(inventory).encode("utf-8"))


def _compare_command(args: argparse.Namespace) -> None:
    inventory_path = Path(args.official_inventory)
    inventory = load_official_inventory(inventory_path)
    manifest, edition, currency = _manifest_selection(
        args.oracle_manifest, inventory.corpus
    )
    if args.snapshot != manifest.snapshot:
        raise SystemExit(
            f"snapshot {args.snapshot!r} differs from oracle registry "
            f"{manifest.snapshot!r}"
        )
    if not edition.staged or edition.local_path is None or edition.sha256 is None:
        raise SystemExit(
            f"{edition.oracle_edition} is not staged in {args.oracle_manifest}; "
            "a URL without verified local bytes cannot support a coverage baseline"
        )
    inventory_identity = (
        inventory.oracle_edition,
        inventory.oracle_kind,
        inventory.edition_date,
        inventory.source_url,
        inventory.source_sha256,
    )
    registry_identity = (
        edition.oracle_edition,
        edition.kind,
        edition.edition_date,
        edition.source_url,
        edition.sha256,
    )
    if inventory_identity != registry_identity:
        raise SystemExit("official inventory provenance differs from the oracle registry")
    try:
        observed_oracle_sha, observed_hash_method = oracle_source_sha256(
            edition.local_path
        )
    except ValueError as exc:
        raise SystemExit(f"staged official source cannot be verified: {exc}") from exc
    if observed_oracle_sha != edition.sha256:
        raise SystemExit("staged official source bytes differ from the oracle registry")
    if inventory.source_hash_method != observed_hash_method:
        raise SystemExit("official inventory source hash method differs from staged source")
    candidates, evidence = scan_dataset_candidates(
        args.dataset,
        snapshot=args.snapshot,
        dataset_revision=manifest.dataset_revision,
        corpus=inventory.corpus,
        expected_sha256=args.dataset_sha256,
        legal_content_cutoff=currency.snapshot_content_cutoff,
        cutoff_status=currency.cutoff_status,
    )
    baseline = build_baseline(
        inventory,
        inventory_sha256=file_sha256(inventory_path),
        candidates=candidates,
        dataset=evidence,
    )
    Path(args.json_output).write_bytes(render_manifest_json(baseline).encode("utf-8"))
    Path(args.markdown_output).write_bytes(render_markdown(baseline).encode("utf-8"))


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="COV-1A official-denominator USC/CFR provision baseline"
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)

    inventory_parser = subparsers.add_parser(
        "build-inventory", help="project pinned official XML/ZIP into a provision inventory"
    )
    inventory_parser.add_argument("--corpus", choices=tuple(FederalCorpus), required=True)
    inventory_parser.add_argument("--oracle-manifest", required=True)
    inventory_parser.add_argument("--output", required=True)
    inventory_parser.add_argument("--title-cutoffs")
    inventory_parser.add_argument(
        "--currency-basis",
        required=True,
        help="human-auditable basis applied to each title currency record",
    )
    inventory_parser.set_defaults(handler=_build_inventory_command)

    compare_parser = subparsers.add_parser(
        "compare", help="compare Open US Law with a normalized official inventory"
    )
    compare_parser.add_argument("--official-inventory", required=True)
    compare_parser.add_argument("--oracle-manifest", required=True)
    compare_parser.add_argument("--dataset", required=True)
    compare_parser.add_argument("--dataset-sha256", required=True)
    compare_parser.add_argument("--snapshot", required=True)
    compare_parser.add_argument("--json-output", required=True)
    compare_parser.add_argument("--markdown-output", required=True)
    compare_parser.set_defaults(handler=_compare_command)

    args = parser.parse_args(argv)
    args.handler(args)


if __name__ == "__main__":
    main()
