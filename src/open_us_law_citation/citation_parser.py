"""M2 — federal exact-citation detector + parser (oracle-independent slice).

Deterministically turn a USC citation (``42 U.S.C. § 1983``) or a CFR citation
(``17 CFR 240.10b-5``), plus supported variants, into a structured ``ParsedCitation``
and — when anchored to a source row or a scanned span — a ``ReferenceMention``. This is
the parsing half of M2; **resolution to a target ``legal_id`` (M3), the alias index, and
official-oracle validation are out of scope** — a mention is pre-resolution structure only.

Grammar, not guesswork. Every parse function returns ``None`` (abstains) rather than emit
a low-confidence guess — an explicit non-parse beats a wrong structured claim, matching the
project's "abstain rather than guess" invariant. A rule-derived mention carries its
``parser_method`` and a ``DerivedArtifactProvenance`` so it is never indistinguishable from
a future model-derived one, and it sits on the interpretation side of the versioned
boundary (zero effect on ``source_record_id`` / ``raw_text_hash``).

Supported today (``reference_type`` ``ABSOLUTE``/``QUALIFIED`` only; hierarchy-relative
``LOCAL``/``RELATIVE``/``CONTAINER`` are the hierarchy resolver's / M4's job):

* USC — ``42 U.S.C. § 1983``, ``42 USC 1983``, ``42 U.S.C. 1983``, ``42 U.S.C.A. § 1983``,
  a trailing ``(2024)``, letter-suffix sections (``1613a``, ``77aa``, ``1749aaa``),
  underscore tails (``222e_2``), subsections (``§ 1983(a)(2)``), and the qualified
  ``section 1983 of title 42``.
* CFR (``cfr_grammar_v3``) — ``17 CFR 240.10b-5``, ``5 C.F.R. § 330.601``, hyphen/letter
  sections (``1864.0-3``), letter-suffixed parts (``261a.1``), hyphenated FPMR parts
  (``101-6.2104``), a trailing ``(2026)``, and ``section 240.10b-5 of title 17``. Unlike
  USC, a CFR section's parenthesised/temporary material is part of its identity, so the CFR
  grammar keeps it in ``parsed_section`` (``41.6151(a)-1``, ``240.11a1-4(T)``). A few parts
  number their sections without the ``part.section`` dot (14 CFR Part 241: ``1-1``, ``03``);
  those parse with ``parsed_part=None`` at reduced confidence.

**Self-check (the Stage-B metric on the dataset's own labels).** Every USC/CFR row carries
a regular ``citation`` / ``citation_short`` string *and* structured ``title_number`` /
``section_number`` ground truth, so parsing each self-citation and comparing the parsed
components to the structured fields measures parse accuracy at full-corpus scale with no
external oracle. Reads only the small metadata columns (never ``text``), so it is OOM-safe.

Regenerate the report::

    uv run python -m open_us_law_citation.citation_parser \\
        data/v2026.08_full/us_federal_statutes.parquet \\
        data/v2026.08_full/us_federal_regulations.parquet \\
        --snapshot v2026.08 --out reports/M2_parse_selfcheck.md
"""

from __future__ import annotations

import argparse
import glob as globlib
import hashlib
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Iterator, Sequence

import pyarrow.parquet as pq

from .coverage_baseline import TITLE_MAX, FederalCorpus, title_in_range
from .derived import (
    ArtifactInput,
    ArtifactType,
    DerivedArtifactProvenance,
    InputType,
    assign_payload_hash,
)

# Columns the self-check needs — deliberately excludes ``text`` (OOM invariant).
_SELFCHECK_COLUMNS = [
    "act_id",
    "citation",
    "citation_short",
    "title_number",
    "section_number",
]


class ReferenceType(StrEnum):
    """How a reference addresses its target.

    Only ``ABSOLUTE`` and ``QUALIFIED`` are produced by the M2 grammar. The
    hierarchy-relative kinds are reserved for the hierarchy resolver / M4 and are
    never emitted here.
    """

    ABSOLUTE = "absolute"       # fully self-contained: "42 U.S.C. § 1983"
    QUALIFIED = "qualified"     # "section 1983 of title 42"
    LOCAL = "local"             # reserved (hierarchy resolver)
    RELATIVE = "relative"       # reserved (hierarchy resolver)
    CONTAINER = "container"     # reserved (hierarchy resolver)


# ---------------------------------------------------------------------------
# Structured parse.
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ParsedCitation:
    """The structured components a citation string parses into (pre-resolution)."""

    parsed_corpus: FederalCorpus
    parsed_title: str
    parsed_section: str
    reference_type: ReferenceType
    parser_method: str
    parser_confidence: float
    parsed_part: str | None = None          # CFR part (digits before the first dot)
    parsed_subsection: str | None = None    # e.g. "(a)(2)"
    parsed_jurisdiction: str = "US"

    def __post_init__(self) -> None:
        if not isinstance(self.parsed_corpus, FederalCorpus):
            raise ValueError("parsed_corpus must be a FederalCorpus")
        if not isinstance(self.reference_type, ReferenceType):
            raise ValueError("reference_type must be a ReferenceType")
        if self.reference_type not in (ReferenceType.ABSOLUTE, ReferenceType.QUALIFIED):
            raise ValueError("M2 grammar only emits ABSOLUTE/QUALIFIED references")
        if not str(self.parsed_title).isdigit():
            raise ValueError(f"parsed_title must be a title number, got {self.parsed_title!r}")
        if not title_in_range(self.parsed_corpus, self.parsed_title):
            raise ValueError(
                f"{self.parsed_corpus} has no title {self.parsed_title} "
                f"(1-{TITLE_MAX[self.parsed_corpus]})"
            )
        if not self.parsed_section.strip():
            raise ValueError("parsed_section must be non-empty")
        if not self.parser_method:
            raise ValueError("parser_method must be non-empty")
        if not (0.0 <= self.parser_confidence <= 1.0):
            raise ValueError("parser_confidence must be in [0, 1]")
        # A USC citation never carries a part. A CFR citation usually does, but the
        # dotless forms (14 CFR Part 241) legitimately leave it None — the part is not in
        # the citation string — so CFR part is optional, not required.
        if self.parsed_corpus == FederalCorpus.USC and self.parsed_part is not None:
            raise ValueError("a USC citation has no part")


# ---------------------------------------------------------------------------
# Grammar. Deterministic regexes; abstention (``None``) is a first-class outcome.
#
# ``§`` may be doubled (``§§``) or spelled ``Section`` / ``Sec.``; periods and inner
# spaces in ``U.S.C.`` / ``C.F.R.`` are optional; an ``A`` suffix (``U.S.C.A.``) is the
# annotated reporter. A trailing ``(YYYY)`` edition marker is optional and discarded.
# ---------------------------------------------------------------------------

_USC_CODE = r"U\.?\s?S\.?\s?C\.?(?:\s?A\.?)?"        # U.S.C., USC, U.S.C.A.
_CFR_CODE = r"C\.?\s?F\.?\s?R\.?"                    # C.F.R., CFR
_SECTION_SIGN = r"(?:§{1,2}|[Ss]ections?|[Ss]ecs?\.?)"
_YEAR = r"(?:\s*\((?:19|20)\d{2}\))?"

# USC section: digits, then optional letter suffix (1613a, 77aa, 1749aaa) and an
# optional underscore-number tail (222e_2). No dots. A USC subsection (``(a)(2)``) is a
# *separate* pointer — the dataset's section_number is the bare number — so USC keeps the
# ``_USC_SUBSEC`` group and strips it out of ``parsed_section``.
_USC_SECTION = r"(?P<section>\d+[A-Za-z]*(?:_\d+)?)"
# CFR section (cfr_grammar_v3): part.rest, where the ENTIRE token is the section identity.
# Unlike USC, the dataset stores parenthesised/temporary material *inside* section_number
# (26 CFR § 41.6151(a)-1, 17 CFR § 240.11a1-4(T)), so it captures embedded ``(...)`` and a
# trailing ``(T)`` as part of the section rather than stripping them. The part may carry a
# letter suffix (261a.1) or hyphenated FPMR segments (101-6.2104); the token must end on an
# alphanumeric or ``)`` so sentence punctuation in free text is not swallowed. A ``(YYYY)``
# edition marker is always space-separated, so it is never captured here.
_USC_SUBSEC = r"(?P<subsection>(?:\([0-9A-Za-z]{1,4}\))+)?"
_CFR_SECTION = (
    r"(?P<section>(?P<part>\d+[A-Za-z]?(?:-\d+[A-Za-z]?)*)"
    r"\.[0-9A-Za-z](?:[0-9A-Za-z().\-]*[0-9A-Za-z)])?)"
)

_USC_ABSOLUTE = re.compile(
    rf"(?P<title>\d+)\s+{_USC_CODE}\s*(?:{_SECTION_SIGN}\s*)?{_USC_SECTION}{_USC_SUBSEC}{_YEAR}",
)
_USC_QUALIFIED = re.compile(
    rf"[Ss]ection\s+{_USC_SECTION}{_USC_SUBSEC}\s+of\s+[Tt]itle\s+(?P<title>\d+)"
    rf"(?:,?\s+United\s+States\s+Code)?",
)
_CFR_ABSOLUTE = re.compile(
    rf"(?P<title>\d+)\s+{_CFR_CODE}\s*(?:{_SECTION_SIGN}\s*)?{_CFR_SECTION}{_YEAR}",
)
_CFR_QUALIFIED = re.compile(
    rf"[Ss]ection\s+{_CFR_SECTION}\s+of\s+[Tt]itle\s+(?P<title>\d+)"
    rf"(?:,?\s+Code\s+of\s+Federal\s+Regulations)?",
)
# Dotless CFR section (cfr_grammar_v3): a few parts number their sections WITHOUT the
# standard `part.section` dot — 14 CFR Part 241 (airline Uniform System of Accounts) uses
# `1-1`, `03`, `19-4`, etc. The citation string then carries only the section, so the part
# is NOT determinable from the string (``parsed_part=None``) and confidence is reduced. The
# form is inherently more ambiguous (a bare number can also be a part reference), so it is
# only tried after the dotted forms fail, and is deliberately excluded from the free-text
# detector (``detect_mentions``) where that ambiguity would produce false positives.
_CFR_DOTLESS = re.compile(
    rf"(?P<title>\d+)\s+{_CFR_CODE}\s*(?:{_SECTION_SIGN}\s*)?"
    rf"(?P<section>\d+[A-Za-z]?(?:-\d+[A-Za-z]?)*){_YEAR}",
)

# Confidence: a fully-punctuated canonical form is 1.0; the qualified prose form is
# slightly lower; a dotless CFR section is lower still (no part, more ambiguous), but the
# parse of what IS present stays deterministic.
_ABSOLUTE_CONFIDENCE = 1.0
_QUALIFIED_CONFIDENCE = 0.9
_DOTLESS_CONFIDENCE = 0.75


def _parsed_from_absolute(
    m: re.Match,
    corpus: FederalCorpus,
    method: str,
    confidence: float = _ABSOLUTE_CONFIDENCE,
) -> ParsedCitation | None:
    if not title_in_range(corpus, m.group("title")):
        return None  # not a real title: abstain rather than emit a citation to nothing
    return ParsedCitation(
        parsed_corpus=corpus,
        parsed_title=m.group("title"),
        parsed_section=m.group("section"),
        # ``.get`` (not ``.group``) so the dotless CFR form, which has no ``part`` group,
        # yields ``parsed_part=None`` rather than raising.
        parsed_part=m.groupdict().get("part") if corpus == FederalCorpus.CFR else None,
        parsed_subsection=m.groupdict().get("subsection") or None,
        reference_type=ReferenceType.ABSOLUTE,
        parser_method=method,
        parser_confidence=confidence,
    )


def _parsed_from_qualified(
    m: re.Match, corpus: FederalCorpus, method: str
) -> ParsedCitation | None:
    if not title_in_range(corpus, m.group("title")):
        return None
    return ParsedCitation(
        parsed_corpus=corpus,
        parsed_title=m.group("title"),
        parsed_section=m.group("section"),
        parsed_part=m.group("part") if corpus == FederalCorpus.CFR else None,
        parsed_subsection=m.groupdict().get("subsection") or None,
        reference_type=ReferenceType.QUALIFIED,
        parser_method=method,
        parser_confidence=_QUALIFIED_CONFIDENCE,
    )


def _fullmatch(pattern: re.Pattern, text: str) -> re.Match | None:
    """Match the whole trimmed string (ignoring surrounding whitespace)."""
    return pattern.fullmatch(text.strip())


def parse_usc_citation(text: str) -> ParsedCitation | None:
    """Parse a single USC citation string, or abstain (``None``)."""
    m = _fullmatch(_USC_ABSOLUTE, text)
    if m:
        return _parsed_from_absolute(m, FederalCorpus.USC, "usc_grammar_v1")
    m = _fullmatch(_USC_QUALIFIED, text)
    if m:
        return _parsed_from_qualified(m, FederalCorpus.USC, "usc_grammar_v1")
    return None


def parse_cfr_citation(text: str) -> ParsedCitation | None:
    """Parse a single CFR citation string, or abstain (``None``).

    Dotted ``part.section`` forms are tried first; only if those fail is the dotless form
    (14 CFR Part 241's ``1-1`` / ``03`` numbering) attempted, at reduced confidence with
    ``parsed_part=None`` — the part is not present in the string to recover.
    """
    m = _fullmatch(_CFR_ABSOLUTE, text)
    if m:
        return _parsed_from_absolute(m, FederalCorpus.CFR, "cfr_grammar_v3")
    m = _fullmatch(_CFR_QUALIFIED, text)
    if m:
        return _parsed_from_qualified(m, FederalCorpus.CFR, "cfr_grammar_v3")
    m = _fullmatch(_CFR_DOTLESS, text)
    if m:
        return _parsed_from_absolute(
            m, FederalCorpus.CFR, "cfr_grammar_v3", confidence=_DOTLESS_CONFIDENCE
        )
    return None


def parse_citation(text: str) -> ParsedCitation | None:
    """Parse a USC or CFR citation string, or abstain. CFR is tried first because its
    ``C.F.R.`` token is unambiguous; a USC form never matches the CFR grammar."""
    return parse_cfr_citation(text) or parse_usc_citation(text)


# ---------------------------------------------------------------------------
# ReferenceMention — the anchored, provenance-carrying artifact (M2).
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ReferenceMention:
    """A parsed citation occurrence, anchored to where it was found.

    Carries a ``DerivedArtifactProvenance`` (a ``source_record`` edge when found
    in-body, no edge for a standalone query) and a ``payload_hash`` like every derived
    artifact, so the D2 collision tripwire covers it and a rule-derived mention is never
    stored indistinguishably from a future model-derived one.
    """

    parsed: ParsedCitation
    raw_reference_text: str
    start_char: int
    end_char: int
    provenance: DerivedArtifactProvenance
    payload_hash: str = ""
    source_record_id: str | None = None
    source_legal_id: str | None = None
    structural_path: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.parsed, ParsedCitation):
            raise ValueError("parsed must be a ParsedCitation")
        if self.start_char < 0 or self.end_char < self.start_char:
            raise ValueError("invalid character span")
        if self.provenance.artifact_type != ArtifactType.REFERENCE_MENTION:
            raise ValueError("provenance.artifact_type must be reference_mention")
        # A source-record edge, if present, must name this mention's source record.
        edges = self.provenance.source_record_ids()
        if self.source_record_id is not None and edges != (self.source_record_id,):
            raise ValueError("provenance source_record edge must equal source_record_id")
        if self.source_record_id is None and edges:
            raise ValueError("a standalone mention must carry no source_record edge")
        assign_payload_hash(self, ArtifactType.REFERENCE_MENTION, self._payload())

    def _payload(self) -> dict[str, Any]:
        p = self.parsed
        return {
            "parsed": {
                "corpus": p.parsed_corpus,
                "jurisdiction": p.parsed_jurisdiction,
                "title": p.parsed_title,
                "part": p.parsed_part,
                "section": p.parsed_section,
                "subsection": p.parsed_subsection,
                "reference_type": p.reference_type,
                "parser_method": p.parser_method,
                "parser_confidence": p.parser_confidence,
            },
            "raw_reference_text": self.raw_reference_text,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "source_record_id": self.source_record_id,
            "source_legal_id": self.source_legal_id,
            "structural_path": self.structural_path,
        }


_PRODUCER_VERSION = "1"


def _mention_config_hash(
    parsed: ParsedCitation, start_char: int, end_char: int, raw_reference_text: str
) -> str:
    """Distinguish co-located mentions within one derivation address.

    ``artifact_id`` is ``hash(inputs, producer, version, config_hash)``, so two distinct
    citations found in the *same* source record (same source_record edge, same producer)
    would otherwise collide. Folding the occurrence's span + parsed identity into
    ``config_hash`` gives each distinct mention a distinct id while a re-derivation of the
    *same* occurrence stays stable.
    """
    key = "\x1f".join(
        str(x)
        for x in (
            start_char,
            end_char,
            parsed.parsed_corpus,
            parsed.parsed_title,
            parsed.parsed_part,
            parsed.parsed_section,
            parsed.parsed_subsection,
            parsed.reference_type,
            raw_reference_text,
        )
    )
    return "cfg:sha256:" + hashlib.sha256(key.encode("utf-8")).hexdigest()


def build_reference_mention(
    parsed: ParsedCitation,
    raw_reference_text: str,
    start_char: int,
    end_char: int,
    *,
    source_record_id: str | None = None,
    source_legal_id: str | None = None,
    structural_path: str | None = None,
    generated_at: str | None = None,
) -> ReferenceMention:
    """Construct a ``ReferenceMention`` with provenance keyed to ``parser_method``."""
    inputs: tuple[ArtifactInput, ...] = ()
    if source_record_id is not None:
        inputs = (ArtifactInput(InputType.SOURCE_RECORD, source_record_id),)
    provenance = DerivedArtifactProvenance.build(
        ArtifactType.REFERENCE_MENTION,
        inputs,
        producer_name=parsed.parser_method,
        producer_version=_PRODUCER_VERSION,
        config_hash=_mention_config_hash(parsed, start_char, end_char, raw_reference_text),
        generated_at=generated_at,
    )
    return ReferenceMention(
        parsed=parsed,
        raw_reference_text=raw_reference_text,
        start_char=start_char,
        end_char=end_char,
        provenance=provenance,
        source_record_id=source_record_id,
        source_legal_id=source_legal_id,
        structural_path=structural_path,
    )


# Detection scan: the same grammar, unanchored, over free text.
_DETECT_USC = re.compile(_USC_ABSOLUTE.pattern)
_DETECT_CFR = re.compile(_CFR_ABSOLUTE.pattern)

# Qualified prose form in free text ("section 1983 of title 42, United States Code"). Unlike
# explicit parsing — where the reader already believes the string is a citation, so the code
# name is optional — DETECTION must require the spelled-out code name (or its abbreviation) to
# stay precise: "section 5 of title I of the Act" / "section 1983 of title 42 of the lease"
# are NOT citations and carry no such tail, so they never fire here.
_USC_CODE_NAME = r"(?:United\s+States\s+Code|U\.?\s?S\.?\s?C\.?(?:\s?A\.?)?)"
_CFR_CODE_NAME = r"(?:Code\s+of\s+Federal\s+Regulations|C\.?\s?F\.?\s?R\.?)"
_DETECT_USC_QUALIFIED = re.compile(
    rf"[Ss]ection\s+{_USC_SECTION}{_USC_SUBSEC}\s+of\s+[Tt]itle\s+(?P<title>\d+)"
    rf"(?:\s+of\s+the)?,?\s+{_USC_CODE_NAME}"
)
_DETECT_CFR_QUALIFIED = re.compile(
    rf"[Ss]ection\s+{_CFR_SECTION}\s+of\s+[Tt]itle\s+(?P<title>\d+)"
    rf"(?:\s+of\s+the)?,?\s+{_CFR_CODE_NAME}"
)

# Enumerated `§§ a, b, c` lists. A **plural** section sign (``§§``, ``Sections``, ``Secs``)
# in the primary match licenses consuming further comma/and-separated **bare** sections that
# share the primary's title. The negative lookahead ``_NOT_A_NEW_CITATION`` is the precision
# guard: a section immediately followed by a code (``5`` in ``…, and 5 U.S.C. § 552``) is a
# *new* citation, not a list member, so the list stops there and the new citation is caught
# by the ordinary scan. Only a plural sign triggers this, so a single-``§`` citation followed
# by ``and 5 U.S.C. …`` never mis-attributes ``5`` to the first title.
_PLURAL_SIGN_RE = re.compile(r"§§|[Ss]ections\b|[Ss]ecs\b")
_LIST_SEP = r"(?:\s*,\s*(?:and\s+)?|\s+and\s+)"
_NOT_A_NEW_CITATION = r"(?!\s*(?:U\.?\s?S\.?\s?C|C\.?\s?F\.?\s?R))"
_USC_SECTION_BARE = r"\d+[A-Za-z]*(?:_\d+)?(?:\([0-9A-Za-z]{1,4}\))*"
_CFR_SECTION_BARE = r"\d+[A-Za-z]?(?:-\d+[A-Za-z]?)*\.[0-9A-Za-z](?:[0-9A-Za-z().\-]*[0-9A-Za-z)])?"
_USC_LIST_TAIL = re.compile(rf"{_LIST_SEP}(?P<section>{_USC_SECTION_BARE}){_NOT_A_NEW_CITATION}")
# A USC list member carries its subsection inline (``§§ 154(i), 4(i)``). Split it back out so a
# list member is identical to the same citation written as a primary (which yields section
# ``4`` + subsection ``(i)``) — otherwise one provision produces two different edges. CFR is
# deliberately NOT split: there, parenthesised material is *inside* the section identity.
_USC_LIST_SPLIT = re.compile(
    r"^(?P<section>\d+[A-Za-z]*(?:_\d+)?)(?P<subsection>(?:\([0-9A-Za-z]{1,4}\))*)$"
)
_CFR_LIST_TAIL = re.compile(rf"{_LIST_SEP}(?P<section>{_CFR_SECTION_BARE}){_NOT_A_NEW_CITATION}")
_LIST_TAILS = {FederalCorpus.USC: _USC_LIST_TAIL, FederalCorpus.CFR: _CFR_LIST_TAIL}


def detect_mentions(
    text: str, *, source_record_id: str | None = None, structural_path: str | None = None
) -> list[ReferenceMention]:
    """Scan free text for ABSOLUTE USC/CFR citation spans → ``ReferenceMention``s.

    CFR spans are matched first and USC matches overlapping a CFR span are dropped, so a
    ``C.F.R.`` citation is never double-counted as a bare USC number. An enumerated
    ``§§ a, b`` list emits one mention per member, all sharing the primary's title.
    Deterministic order (by span start).
    """
    mentions: list[ReferenceMention] = []
    spans: list[tuple[int, int]] = []

    def _emit(parsed: ParsedCitation, raw: str, start: int, end: int) -> None:
        spans.append((start, end))
        mentions.append(
            build_reference_mention(
                parsed, raw, start, end,
                source_record_id=source_record_id, structural_path=structural_path,
            )
        )

    for pattern, corpus, method in (
        (_DETECT_CFR, FederalCorpus.CFR, "cfr_grammar_v3"),
        (_DETECT_USC, FederalCorpus.USC, "usc_grammar_v1"),
    ):
        for m in pattern.finditer(text):
            if any(m.start() < e and s < m.end() for s, e in spans):
                continue
            parsed = _parsed_from_absolute(m, corpus, method)
            if parsed is None:
                continue  # impossible title: emit nothing, and license no list either
            _emit(parsed, m.group(0), m.start(), m.end())
            # Enumerated list: only a plural section sign licenses the continuation.
            if not _PLURAL_SIGN_RE.search(m.group(0)):
                continue
            title = m.group("title")
            pos = m.end()
            while (tm := _LIST_TAILS[corpus].match(text, pos)) is not None:
                section = tm.group("section")
                subsection: str | None = None
                if corpus == FederalCorpus.USC:
                    split = _USC_LIST_SPLIT.match(section)
                    if split is not None:
                        section = split.group("section")
                        subsection = split.group("subsection") or None
                part = section.split(".", 1)[0] if corpus == FederalCorpus.CFR else None
                _emit(
                    ParsedCitation(
                        parsed_corpus=corpus, parsed_title=title, parsed_section=section,
                        parsed_part=part, parsed_subsection=subsection,
                        reference_type=ReferenceType.ABSOLUTE,
                        parser_method=method, parser_confidence=_ABSOLUTE_CONFIDENCE,
                    ),
                    tm.group("section"), tm.start("section"), tm.end("section"),
                )
                pos = tm.end()

    # Qualified prose form ("section 1983 of title 42, United States Code"), code name
    # mandatory. Run after the absolute pass; overlaps with an absolute span are skipped.
    for pattern, corpus, method in (
        (_DETECT_CFR_QUALIFIED, FederalCorpus.CFR, "cfr_grammar_v3"),
        (_DETECT_USC_QUALIFIED, FederalCorpus.USC, "usc_grammar_v1"),
    ):
        for m in pattern.finditer(text):
            if any(m.start() < e and s < m.end() for s, e in spans):
                continue
            parsed = _parsed_from_qualified(m, corpus, method)
            if parsed is None:
                continue
            _emit(parsed, m.group(0), m.start(), m.end())

    mentions.sort(key=lambda mm: (mm.start_char, mm.end_char))
    return mentions


# ---------------------------------------------------------------------------
# Self-check harness (Stage-B metric on the dataset's own labels).
# ---------------------------------------------------------------------------

_NAMESPACE_CORPUS = {"USC": FederalCorpus.USC, "CFR": FederalCorpus.CFR}


def _act_id_namespace(act_id: str | None) -> str:
    if not act_id:
        return "?"
    return act_id.split("_", 1)[0].upper()


@dataclass
class CorpusSelfCheck:
    """Parse outcomes for one act_id namespace within one file."""

    corpus: str
    rows: int = 0
    parsed: int = 0
    exact: int = 0       # parsed AND both structured fields present AND both agree
    recovered: int = 0   # parsed, a structured field was NULL, nothing present disagreed
    mismatch: int = 0    # parsed but a PRESENT structured field disagrees (a real gap)
    abstained: int = 0
    mismatch_examples: list[tuple[str, str, str]] = None  # (citation, parsed, expected)
    abstained_examples: list[str] = None                  # citations that did not parse

    def __post_init__(self) -> None:
        if self.mismatch_examples is None:
            self.mismatch_examples = []
        if self.abstained_examples is None:
            self.abstained_examples = []


def _normalize_section(value: str | None) -> str:
    return (value or "").strip().casefold()


def analyze_file(path: str | Path) -> dict[str, CorpusSelfCheck]:
    """Parse each row's self-citation and compare to its structured fields.

    Only ``USC_*`` / ``CFR_*`` namespace rows are scored (those are the citations the M2
    grammar targets); other namespaces (Federal Register, state) are counted as an
    expected-abstention baseline, not a failure.
    """
    path = Path(path)
    results: dict[str, CorpusSelfCheck] = {
        "USC": CorpusSelfCheck("USC"),
        "CFR": CorpusSelfCheck("CFR"),
        "other": CorpusSelfCheck("other"),
    }
    for row in _iter_rows(path):
        ns = _act_id_namespace(row["act_id"])
        corpus = _NAMESPACE_CORPUS.get(ns)
        bucket = results[ns] if corpus is not None else results["other"]
        bucket.rows += 1

        citation = row["citation_short"] or row["citation"]
        parsed = parse_citation(citation) if citation else None

        if corpus is None:
            # Expected-abstention baseline: a parse here is an over-match to note.
            if parsed is not None:
                bucket.parsed += 1
            else:
                bucket.abstained += 1
            continue

        if parsed is None:
            bucket.abstained += 1
            if citation:
                bucket.abstained_examples.append(citation)
            continue
        bucket.parsed += 1

        title_present = row["title_number"] is not None
        section_present = row["section_number"] is not None
        # A PRESENT structured field that disagrees is a real gap; a null field the parser
        # populated is recovery (the flat columns are unreliable — M0), not a failure.
        corpus_wrong = parsed.parsed_corpus != corpus
        title_disagrees = title_present and str(parsed.parsed_title) != str(row["title_number"])
        section_disagrees = section_present and _normalize_section(
            parsed.parsed_section
        ) != _normalize_section(row["section_number"])

        if corpus_wrong or title_disagrees or section_disagrees:
            bucket.mismatch += 1
            expected = f"T{row['title_number']} S{row['section_number']!r}"
            got = f"T{parsed.parsed_title} S{parsed.parsed_section!r}"
            bucket.mismatch_examples.append((citation, got, expected))
        elif title_present and section_present:
            bucket.exact += 1
        else:
            bucket.recovered += 1
    return results


def _iter_rows(path: Path) -> Iterator[dict[str, Any]]:
    pf = pq.ParquetFile(path)
    for batch in pf.iter_batches(columns=_SELFCHECK_COLUMNS):
        cols = {name: batch.column(name).to_pylist() for name in _SELFCHECK_COLUMNS}
        for i in range(batch.num_rows):
            yield {name: cols[name][i] for name in _SELFCHECK_COLUMNS}


def _pct(numer: int, denom: int) -> str:
    return f"{100.0 * numer / denom:.2f}%" if denom else "—"


# Embedded qualitative findings (like hierarchy.py's EXIT_SECTION) so the report
# regenerates verbatim. These are the citation-format facts the self-check rests on —
# each conformance figure below was measured over the full v2026.08 federal corpus.
_FORMAT_SECTION = """\
## Citation format (what the grammar targets)

Each row stores `citation` (with edition year) and `citation_short` (without). For USC and
codified CFR the shape is exact and uniform across the whole corpus:

```
citation        =  citation_short + " (" + year + ")"
citation_short  =  <title> <CODE> § <section>
```

| Corpus | Rows | Template | Example (`citation`) | Conformance |
|---|---:|---|---|---:|
| USC | 54,853 | `<title> U.S.C. § <section> (<year>)` | `42 U.S.C. § 1983 (2024)` | 100.00% |
| CFR (codified) | 220,018 | `<title> C.F.R. § <section> (<year>)` | `5 C.F.R. § 330.601 (2026)` | 100.00% |
| Federal Register (`FR_*`) | 362,036 | `<volume> FR <page>` | `71 FR 8523` | different format |

- `citation_short` matches `^<n> U.S.C. § ` for 100% of USC rows and `^<n> C.F.R. § ` for
  100% of codified CFR rows; `citation == citation_short || ' (' || year || ')'` holds for
  100% of both (and for none of the FR rows).
- The USC edition `<year>` is uniformly `2024` (the GovInfo USCODE-2024 edition); CFR carries
  its source year.
- Federal Register is a `volume FR page` locator (`71 FR 8523`) — no `§`, no title/section —
  so all 362,036 `FR_*` rows are excluded from the parser (promulgation records, not codified
  sections) and form the expected-abstention baseline above.

### The `<section>` sub-grammar (the one component with real structure)

| Corpus | Shape | Examples |
|---|---|---|
| USC | digits + optional letters + optional `_digits` | `1983`, `1613a`, `77aa`, `1749aaa`, `222e_2` |
| CFR | `part.rest`; part may carry a letter (`261a`) or hyphens (`101-6`); rest carries digits/letters/hyphens and **embedded** `(...)` / `(T)` | `330.601`, `240.10b-5`, `1864.0-3`, `41.6151(a)-1`, `240.11a1-4(T)` |

The load-bearing USC-vs-CFR asymmetry (why the CFR producer is `cfr_grammar_v3`): in USC a
subsection like `(a)` is a *separate* pointer and never appears in `section_number`; in CFR
the parenthesised/`(T)` material is *part of the section identity* and lives inside
`section_number`, so v2 keeps it in `parsed_section`.

Beyond the `§` forms, the grammar also accepts the variants people write — `42 USC 1983`,
`42 U.S.C.A. § 1983`, `Section 1983 of Title 42` — but the two fields above are the dataset's
own canonical shape, which is what makes them a clean full-corpus labelled set. A few parts
(14 CFR Part 241) number their sections without the `part.section` dot (`1-1`, `03`, `19-4`);
those parse with `parsed_part=None` at reduced confidence, since the part is not present in
the citation to recover. The only strings that still do not fit are a handful of malformed
source citations (stray spaces, `(Rule N)` annotations) — abstention there is correct.
"""


def render_report(
    per_file: list[tuple[str, dict[str, CorpusSelfCheck]]], snapshot: str
) -> str:
    lines: list[str] = []
    A = lines.append
    A("# M2 citation-parser self-check")
    A("")
    A(f"Snapshot: `{snapshot}`. Parser methods: `usc_grammar_v1`, `cfr_grammar_v3`.")
    A("")
    A("Each USC/CFR row's own `citation_short` (or `citation`) is parsed and its")
    A("`(title, section)` compared to the row's structured `title_number` /")
    A("`section_number` — the Stage-B parse metric on the dataset's own labels, with no")
    A("external oracle. `exact` = parsed and both structured fields present and agree;")
    A("`recovered` = parsed where a structured field was **null** and nothing present")
    A("disagreed (the parser backfills the unreliable flat columns — an M0 finding);")
    A("`mismatch` = a *present* structured field disagrees (a real grammar gap, never")
    A("coerced); `abstained` = no confident parse. Non-USC/CFR namespaces are an")
    A("expected-abstention baseline, not scored.")
    A("")
    for corpus_key in ("USC", "CFR"):
        A(f"## {corpus_key}")
        A("")
        A("| File | Rows | Parsed | Exact | Recovered | Mismatch | Abstained | Correct rate |")
        A("|---|---:|---:|---:|---:|---:|---:|---:|")
        tot = CorpusSelfCheck(corpus_key)
        for fname, results in per_file:
            r = results[corpus_key]
            if r.rows == 0:
                continue
            A(
                f"| {fname} | {r.rows:,} | {r.parsed:,} | {r.exact:,} | {r.recovered:,} "
                f"| {r.mismatch:,} | {r.abstained:,} | {_pct(r.exact + r.recovered, r.rows)} |"
            )
            tot.rows += r.rows
            tot.parsed += r.parsed
            tot.exact += r.exact
            tot.recovered += r.recovered
            tot.mismatch += r.mismatch
            tot.abstained += r.abstained
            tot.mismatch_examples.extend(r.mismatch_examples)
            tot.abstained_examples.extend(r.abstained_examples)
        A(
            f"| **all** | **{tot.rows:,}** | **{tot.parsed:,}** | **{tot.exact:,}** "
            f"| **{tot.recovered:,}** | **{tot.mismatch:,}** | **{tot.abstained:,}** "
            f"| **{_pct(tot.exact + tot.recovered, tot.rows)}** |"
        )
        A("")
        if tot.mismatch_examples:
            A(f"Mismatch examples ({corpus_key}, first 15 by citation):")
            A("")
            A("| Citation | Parsed | Expected |")
            A("|---|---|---|")
            for citation, got, expected in sorted(set(tot.mismatch_examples))[:15]:
                A(f"| `{citation}` | `{got}` | `{expected}` |")
            A("")
        if tot.abstained_examples:
            A(f"Abstention examples ({corpus_key}, first 15 by citation):")
            A("")
            for citation in sorted(set(tot.abstained_examples))[:15]:
                A(f"- `{citation}`")
            A("")
    # Expected-abstention baseline for non-USC/CFR namespaces.
    A("## Expected-abstention baseline (non-USC/CFR namespaces)")
    A("")
    A("| File | Rows | Abstained | Over-matched |")
    A("|---|---:|---:|---:|")
    for fname, results in per_file:
        r = results["other"]
        if r.rows == 0:
            continue
        A(f"| {fname} | {r.rows:,} | {r.abstained:,} | {r.parsed:,} |")
    A("")
    A(_FORMAT_SECTION)
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Stage A — detection metrics on a hand-labelled gold set.
#
# The self-check above scores *parsing* on the dataset's own citations. Detection is a
# different task: find citation spans inside free prose, and NOT fire on citation-shaped
# noise. It is scored as precision/recall against a hand-curated gold set — realistic legal
# sentences carrying USC/CFR citations, plus adversarial distractors (dates, dollar amounts,
# Rule 12(b)(6), Public Law / Fed. Reg. numbers, version strings, phone numbers) whose gold
# is empty. Matching is at the (corpus, title, section) identity level, so it measures "did
# we find the right citation," independent of exact byte offsets (spans are checked in the
# unit suite). Gold labels are independent ground truth, authored to be adversarial — never
# derived from the detector's own output.
# ---------------------------------------------------------------------------

# Each entry: (passage, citations that SHOULD be detected). An empty tuple = a pure
# distractor passage (any detection there is a false positive).
_Cite = tuple[str, str, str]  # (corpus, title, section)
DETECTION_GOLD: tuple[tuple[str, tuple[_Cite, ...]], ...] = (
    ("The claim arises under 42 U.S.C. § 1983.", (("usc", "42", "1983"),)),
    ("See 17 CFR 240.10b-5 for the antifraud rule.", (("cfr", "17", "240.10b-5"),)),
    ("Both 42 U.S.C. § 1983 and 5 U.S.C. § 552 apply.",
     (("usc", "42", "1983"), ("usc", "5", "552"))),
    ("Attorney's fees under 42 U.S.C. § 1988(b) are available.", (("usc", "42", "1988"),)),
    ("Exempt under 26 U.S.C. § 501(c)(3) rules.", (("usc", "26", "501"),)),
    ("It violated 15 U.S.C. § 78j and 17 C.F.R. § 240.10b-5.",
     (("usc", "15", "78j"), ("cfr", "17", "240.10b-5"))),
    ("A proceeding under 42 USC 1983 without periods.", (("usc", "42", "1983"),)),
    ("Citing 42 U.S.C.A. § 1983 (annotated reporter).", (("usc", "42", "1983"),)),
    ("5 C.F.R. § 330.601 governs appointments.", (("cfr", "5", "330.601"),)),
    ("See 43 C.F.R. § 1864.0-3 and nothing else.", (("cfr", "43", "1864.0-3"),)),
    ("Compliance is required by 29 U.S.C. § 651.", (("usc", "29", "651"),)),
    ("Emission limits in 40 C.F.R. § 60.4 apply here.", (("cfr", "40", "60.4"),)),
    ("The provision at 41 C.F.R. § 101-6.2104 (FPMR) applies.", (("cfr", "41", "101-6.2104"),)),
    ("Under 26 C.F.R. § 41.6151(a)-1 a deposit is required.", (("cfr", "26", "41.6151(a)-1"),)),
    ("Compare 12 U.S.C. § 1811 with 12 C.F.R. § 330.1.",
     (("usc", "12", "1811"), ("cfr", "12", "330.1"))),
    ("As amended, 42 U.S.C. § 1983 (2018) still applies.", (("usc", "42", "1983"),)),
    ("Brought under 42 U.S.C. §§ 1983, 1985 jointly.",
     (("usc", "42", "1983"), ("usc", "42", "1985"))),
    ("It cites 42 U.S.C. §§ 1981, 1982, and 1983 together.",
     (("usc", "42", "1981"), ("usc", "42", "1982"), ("usc", "42", "1983"))),
    ("The rules at 17 C.F.R. §§ 240.10b-5, 240.14a-9 apply.",
     (("cfr", "17", "240.10b-5"), ("cfr", "17", "240.14a-9"))),
    # precision trap: a §§ list that runs into a DIFFERENT citation — the "5" must not be
    # mis-attributed to title 42, and 5 U.S.C. § 552 must still be found on its own.
    ("Under 42 U.S.C. §§ 1983, 1985 and 5 U.S.C. § 552, relief lies.",
     (("usc", "42", "1983"), ("usc", "42", "1985"), ("usc", "5", "552"))),
    # qualified prose form — code name present, so it fires
    ("Liability under Section 1983 of Title 42, United States Code, is settled.",
     (("usc", "42", "1983"),)),
    ("As defined in section 552 of title 5 of the United States Code, records.",
     (("usc", "5", "552"),)),
    ("The rule in section 240.10b-5 of title 17, Code of Federal Regulations, applies.",
     (("cfr", "17", "240.10b-5"),)),
    # --- adversarial distractors: nothing should be detected ---
    ("Section 5 of the Agreement dated January 2024.", ()),
    ("Public Law 118-274 amended the statute.", ()),
    ("Published at 89 Fed. Reg. 12,345 (Feb. 1, 2024).", ()),
    ("Rule 12(b)(6) of the Federal Rules of Civil Procedure.", ()),
    ("The software version is 2.10, build 240.10.", ()),
    ("The jury awarded $1,983 in damages plus interest.", ()),
    ("A petition under Chapter 11 of the Bankruptcy Code.", ()),
    ("Regulated under 40 CFR generally, with no section given.", ()),
    ("Please call 1-800-555-1983 for assistance.", ()),
    # qualified-shaped but NOT a citation: no code name -> must not fire
    ("Section 1983 of title 42 of the lease agreement governs.", ()),
    ("Section 5 of title I of the Act controls here.", ()),
    # --- mixed: one real citation alongside citation-shaped noise ---
    ("Under 42 U.S.C. § 1983, not Section 5 of the lease, the claim lies.",
     (("usc", "42", "1983"),)),
    ("89 FR 100 announced the rule now codified at 42 C.F.R. § 480.138.",
     (("cfr", "42", "480.138"),)),
)

# Empirical baseline targets recorded after commissioning (M2 acceptance: thresholds are
# measured, not hardcoded legal rules). The detector is precision-first; with enumerated
# `§§` lists now handled, the gold set has no recall gap (a small floor is kept for slack).
_DETECTION_MIN_PRECISION = 1.0
_DETECTION_MIN_RECALL = 0.98


@dataclass
class DetectionMetrics:
    corpus: str
    tp: int = 0
    fp: int = 0
    fn: int = 0

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) else 1.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) else 1.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) else 0.0


def _mention_key(m: ReferenceMention) -> _Cite:
    return (m.parsed.parsed_corpus.value, m.parsed.parsed_title, m.parsed.parsed_section)


def detection_metrics(
    gold: tuple[tuple[str, tuple[_Cite, ...]], ...] = DETECTION_GOLD,
) -> tuple[dict[str, DetectionMetrics], list[tuple[str, _Cite]], list[tuple[str, _Cite]]]:
    """Score ``detect_mentions`` over ``gold``. Returns (per-corpus metrics incl. 'all',
    false-positive examples, false-negative examples). Citation-identity matching."""
    metrics = {k: DetectionMetrics(k) for k in ("USC", "CFR", "all")}
    fps: list[tuple[str, _Cite]] = []
    fns: list[tuple[str, _Cite]] = []
    for text, expected in gold:
        gold_set = set(expected)
        detected = {_mention_key(m) for m in detect_mentions(text)}
        for cite in detected & gold_set:
            metrics[cite[0].upper()].tp += 1
            metrics["all"].tp += 1
        for cite in detected - gold_set:
            metrics[cite[0].upper()].fp += 1
            metrics["all"].fp += 1
            fps.append((text, cite))
        for cite in gold_set - detected:
            metrics[cite[0].upper()].fn += 1
            metrics["all"].fn += 1
            fns.append((text, cite))
    return metrics, fps, fns


def render_detection_report(
    gold: tuple[tuple[str, tuple[_Cite, ...]], ...] = DETECTION_GOLD,
) -> str:
    metrics, fps, fns = detection_metrics(gold)
    n_passages = len(gold)
    n_distractors = sum(1 for _, c in gold if not c)
    n_gold_cites = sum(len(c) for _, c in gold)
    lines: list[str] = []
    A = lines.append
    A("# M2 citation-detector Stage-A metrics")
    A("")
    A("Detection is scored separately from parsing: find USC/CFR citation spans inside free")
    A("prose (`detect_mentions`), and do **not** fire on citation-shaped noise. The gold set")
    A("is hand-curated — realistic legal sentences plus adversarial distractors (dates,")
    A("dollar amounts, `Rule 12(b)(6)`, Public Law / Fed. Reg. numbers, version strings,")
    A("phone numbers) whose expected result is empty. A detection matches a gold citation on")
    A("its `(corpus, title, section)` identity. Gold labels are independent ground truth,")
    A("never derived from the detector's own output.")
    A("")
    A(f"Gold set: **{n_passages} passages**, **{n_gold_cites} citations**, "
      f"**{n_distractors} pure-distractor passages**.")
    A("")
    A("| Corpus | TP | FP | FN | Precision | Recall | F1 |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for k in ("USC", "CFR", "all"):
        m = metrics[k]
        label = f"**{k}**" if k == "all" else k
        A(f"| {label} | {m.tp} | {m.fp} | {m.fn} | {m.precision:.3f} | "
          f"{m.recall:.3f} | {m.f1:.3f} |")
    A("")
    A("## False positives (precision failures)")
    A("")
    if fps:
        for text, cite in sorted(fps):
            A(f"- `{cite[0]} {cite[1]} {cite[2]}` wrongly detected in: {text!r}")
    else:
        A("None — the detector fired on no distractor.")
    A("")
    A("## False negatives (recall gaps)")
    A("")
    if fns:
        for text, cite in sorted(fns):
            A(f"- `{cite[0]} {cite[1]} {cite[2]}` missed in: {text!r}")
        A("")
        A("The remaining gap is the 2nd+ section of an enumerated `§§ a, b` list — a known,")
        A("deferred detection feature (each list member is a distinct citation).")
    else:
        A("None.")
    A("")
    A("## Empirical baseline targets")
    A("")
    A(f"Recorded after commissioning (not hardcoded legal rules): precision "
      f"`>= {_DETECTION_MIN_PRECISION:.2f}`, recall `>= {_DETECTION_MIN_RECALL:.2f}`. The")
    A("detector is deliberately precision-first — abstaining on ambiguous prose beats a")
    A("false citation edge. The free-text scan covers ABSOLUTE citations, enumerated")
    A("`§§ a, b` lists (each member emitted; a following bare number that is itself a new")
    A("citation is not mis-attributed), and the qualified prose form (`section 1983 of")
    A("title 42, United States Code`) — which fires only when the spelled-out code name is")
    A("present, so `section 5 of title I of the Act` never does. Full corpus-scale in-body")
    A("detection (over the `text` column) is deferred — it overlaps M4.")
    A("")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description="M2: federal exact-citation parser — self-check (parse the dataset's own "
        "citations) and/or Stage-A detection metrics on the hand-labelled gold set."
    )
    ap.add_argument("paths", nargs="*", help="Parquet file(s) or glob(s) for the self-check")
    ap.add_argument("--snapshot", help="snapshot version, e.g. v2026.08 (required with paths)")
    ap.add_argument("--out", help="write the self-check Markdown report here (else stdout)")
    ap.add_argument("--detection-out", help="write the Stage-A detection report here")
    args = ap.parse_args(argv)

    if not args.paths and not args.detection_out:
        ap.error("give Parquet paths (self-check) and/or --detection-out (detection metrics)")

    if args.detection_out:
        Path(args.detection_out).write_text(render_detection_report())
        print(f"wrote {args.detection_out} (detection metrics)")

    if not args.paths:
        return
    if not args.snapshot:
        ap.error("--snapshot is required when Parquet paths are given")

    files = sorted({Path(p) for pat in args.paths for p in globlib.glob(pat)})
    per_file = [(f.name.replace(".parquet", ""), analyze_file(f)) for f in files]
    report = render_report(per_file, args.snapshot)
    if args.out:
        Path(args.out).write_text(report)
        print(f"wrote {args.out} ({len(files)} files)")
    else:
        print(report)


if __name__ == "__main__":
    main()
