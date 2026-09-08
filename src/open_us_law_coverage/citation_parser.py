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
* CFR — ``17 CFR 240.10b-5``, ``5 C.F.R. § 330.601``, hyphen/letter sections
  (``1864.0-3``), letter-suffixed parts (``261a.1``), hyphenated FPMR parts
  (``101-6.2104``), subsections, a trailing ``(2026)``, and
  ``section 240.10b-5 of title 17``.

**Self-check (the Stage-B metric on the dataset's own labels).** Every USC/CFR row carries
a regular ``citation`` / ``citation_short`` string *and* structured ``title_number`` /
``section_number`` ground truth, so parsing each self-citation and comparing the parsed
components to the structured fields measures parse accuracy at full-corpus scale with no
external oracle. Reads only the small metadata columns (never ``text``), so it is OOM-safe.

Regenerate the report::

    uv run python -m open_us_law_coverage.citation_parser \\
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

from .coverage_baseline import FederalCorpus
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
        if not self.parsed_section.strip():
            raise ValueError("parsed_section must be non-empty")
        if not self.parser_method:
            raise ValueError("parser_method must be non-empty")
        if not (0.0 <= self.parser_confidence <= 1.0):
            raise ValueError("parser_confidence must be in [0, 1]")
        if self.parsed_corpus == FederalCorpus.CFR and self.parsed_part is None:
            raise ValueError("a CFR citation must carry parsed_part")
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
_SUBSEC = r"(?P<subsection>(?:\([0-9A-Za-z]{1,4}\))+)?"

# USC section: digits, then optional letter suffix (1613a, 77aa, 1749aaa) and an
# optional underscore-number tail (222e_2). No dots.
_USC_SECTION = r"(?P<section>\d+[A-Za-z]*(?:_\d+)?)"
# CFR section: part.rest. The part may carry a letter suffix (261a.1 -> part 261a) and
# hyphenated segments (101-6.2104 -> part 101-6, the title-41 FPMR style); rest may carry
# letters/hyphens (330.601, 240.10b-5, 1864.0-3, 101-6.205-2).
_CFR_SECTION = (
    r"(?P<section>(?P<part>\d+[A-Za-z]?(?:-\d+[A-Za-z]?)*)\.[0-9A-Za-z][0-9A-Za-z.\-]*)"
)

_USC_ABSOLUTE = re.compile(
    rf"(?P<title>\d+)\s+{_USC_CODE}\s*(?:{_SECTION_SIGN}\s*)?{_USC_SECTION}{_SUBSEC}{_YEAR}",
)
_USC_QUALIFIED = re.compile(
    rf"[Ss]ection\s+{_USC_SECTION}{_SUBSEC}\s+of\s+[Tt]itle\s+(?P<title>\d+)"
    rf"(?:,?\s+United\s+States\s+Code)?",
)
_CFR_ABSOLUTE = re.compile(
    rf"(?P<title>\d+)\s+{_CFR_CODE}\s*(?:{_SECTION_SIGN}\s*)?{_CFR_SECTION}{_SUBSEC}{_YEAR}",
)
_CFR_QUALIFIED = re.compile(
    rf"[Ss]ection\s+{_CFR_SECTION}{_SUBSEC}\s+of\s+[Tt]itle\s+(?P<title>\d+)"
    rf"(?:,?\s+Code\s+of\s+Federal\s+Regulations)?",
)

# Confidence: a fully-punctuated canonical form is 1.0; the qualified prose form is
# slightly lower (more ways to be fooled), but still deterministic.
_ABSOLUTE_CONFIDENCE = 1.0
_QUALIFIED_CONFIDENCE = 0.9


def _parsed_from_absolute(m: re.Match, corpus: FederalCorpus, method: str) -> ParsedCitation:
    return ParsedCitation(
        parsed_corpus=corpus,
        parsed_title=m.group("title"),
        parsed_section=m.group("section"),
        parsed_part=m.group("part") if corpus == FederalCorpus.CFR else None,
        parsed_subsection=m.group("subsection") or None,
        reference_type=ReferenceType.ABSOLUTE,
        parser_method=method,
        parser_confidence=_ABSOLUTE_CONFIDENCE,
    )


def _parsed_from_qualified(m: re.Match, corpus: FederalCorpus, method: str) -> ParsedCitation:
    return ParsedCitation(
        parsed_corpus=corpus,
        parsed_title=m.group("title"),
        parsed_section=m.group("section"),
        parsed_part=m.group("part") if corpus == FederalCorpus.CFR else None,
        parsed_subsection=m.group("subsection") or None,
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
    """Parse a single CFR citation string, or abstain (``None``)."""
    m = _fullmatch(_CFR_ABSOLUTE, text)
    if m:
        return _parsed_from_absolute(m, FederalCorpus.CFR, "cfr_grammar_v1")
    m = _fullmatch(_CFR_QUALIFIED, text)
    if m:
        return _parsed_from_qualified(m, FederalCorpus.CFR, "cfr_grammar_v1")
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


# Detection scan: the same grammar, unanchored, over free text. USC/CFR absolute forms
# only (the qualified prose form is detection-noisy; kept to explicit parsing for now).
_DETECT_USC = re.compile(_USC_ABSOLUTE.pattern)
_DETECT_CFR = re.compile(_CFR_ABSOLUTE.pattern)


def detect_mentions(
    text: str, *, source_record_id: str | None = None, structural_path: str | None = None
) -> list[ReferenceMention]:
    """Scan free text for ABSOLUTE USC/CFR citation spans → ``ReferenceMention``s.

    CFR spans are matched first and USC matches overlapping a CFR span are dropped, so a
    ``C.F.R.`` citation is never double-counted as a bare USC number. Deterministic order
    (by span start).
    """
    mentions: list[ReferenceMention] = []
    spans: list[tuple[int, int]] = []

    for pattern, corpus, method in (
        (_DETECT_CFR, FederalCorpus.CFR, "cfr_grammar_v1"),
        (_DETECT_USC, FederalCorpus.USC, "usc_grammar_v1"),
    ):
        for m in pattern.finditer(text):
            if any(m.start() < e and s < m.end() for s, e in spans):
                continue
            parsed = _parsed_from_absolute(m, corpus, method)
            spans.append((m.start(), m.end()))
            mentions.append(
                build_reference_mention(
                    parsed,
                    m.group(0),
                    m.start(),
                    m.end(),
                    source_record_id=source_record_id,
                    structural_path=structural_path,
                )
            )
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


def render_report(
    per_file: list[tuple[str, dict[str, CorpusSelfCheck]]], snapshot: str
) -> str:
    lines: list[str] = []
    A = lines.append
    A("# M2 citation-parser self-check")
    A("")
    A(f"Snapshot: `{snapshot}`. Parser methods: `usc_grammar_v1`, `cfr_grammar_v1`.")
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
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description="M2: federal exact-citation parser self-check — parse each row's own "
        "citation and compare to its structured title/section."
    )
    ap.add_argument("paths", nargs="+", help="Parquet file(s) or glob(s)")
    ap.add_argument("--snapshot", required=True, help="snapshot version, e.g. v2026.08")
    ap.add_argument("--out", help="write the Markdown report here (else stdout)")
    args = ap.parse_args(argv)

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
