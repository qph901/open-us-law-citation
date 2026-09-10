"""Within-record text integrity — the repeated-span detector.

**Not** :mod:`open_us_law_citation.text_integrity`, which is the top-level report
harness (lowercase starts, amendment banners, impossible citation titles). This is
its derived-artifact counterpart: a per-record conclusion carrying provenance and a
``payload_hash``, on the interpretation side of the versioned boundary.

The defect it exists for
------------------------
COV-1A measured 63,224 single-candidate CFR sections whose text disagrees with the
pinned official edition (29.5%). The dominant cause is **not** missing law, staleness,
or normalization: the dataset re-emits a block of the row's own text. Every observed
block is 395-402 characters, sits across a newline, and 89% of them begin mid-sentence
— several mid-word. That is a fixed-offset window, not a semantic boundary, and it is
consistent with chunk overlap surviving reconstruction into whole sections.

Two properties make this worth its own artifact:

* **It is decidable from the snapshot alone.** A repeated span is visible in the row's
  own bytes, so no oracle, no pinned edition, and no network are involved. That matters
  because the same signature appears well beyond the corpus COV-1A can measure — it is
  present in ``us_federal_statutes`` and state corpora, for which no official oracle is
  staged and, for most states, none exists.
* **It is a *within-record* relation.** ``quality.duplicate_row`` is a *cross-record*
  conclusion scoped to a complete identity group, and its provenance contract requires
  exactly ``[scope, target]`` edges precisely so a sibling-set change re-hashes every
  conclusion. That contract answers a different question and must not be bent to carry
  this one, so this annotation is its own type with exactly one edge: its record.

What it does NOT do
-------------------
It **detects**; it does not repair, and it emits no repaired text. Removing a span is a
separate versioned producer with its own acceptance evidence and an output-to-source
span map — offsets shift, and consumers that store character offsets
(:mod:`..citation_parser`) must translate through that map rather than reuse repaired
offsets as raw ones. Detection also certifies nothing about the *rest* of the row: a
row with no repeated span may still be truncated, stale, or wrong.

Repeated legal language is real (definitions restated across subparts, parallel
findings), which is why the detector requires an **exact** repeat of a long block
immediately across a separator rather than any similarity, and why the flag names an
observation — a span repeated here — instead of asserting the text is wrong.

Measured against the oracle
---------------------------
CFR is the one corpus with independent ground truth, so the detector was scored on it
before being trusted anywhere else. On a deterministic hash-ordered sample of 993
represented sections — **balanced by construction**, 498 the oracle calls mismatched
and 495 it calls agreeing:

===========================  =========  ========
detector                     mismatch   agrees
===========================  =========  ========
flags ``repeated_span``            497         0
clear                                1       495
===========================  =========  ========

Precision 1.0000, recall 0.9980. **Zero false positives**: nothing the oracle calls
correct was flagged, which is the error that matters, because a false flag would
label sound law as damaged. The lone miss (``41 CFR 60-300.40``) is not a duplication
at all — it is the ``<XREF>`` amendment-notice defect in *our* official projection,
where the dataset row is right and the comparison is wrong. Against the defect this
producer exists for, the sample recall is 498/498.

That is a sample, not a proof. M2's Stage-A detector scored 1.000/1.000 on a 36-passage
gold set and still had two defect classes at corpus scale, so treat these numbers as
"no counter-example found in 993 sections," and re-score whenever the window moves or
a new snapshot lands.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Iterable, Protocol

from .provenance import (
    ArtifactType,
    DerivedArtifactProvenance,
    Evidence,
    assign_payload_hash,
    require_enum_member,
    source_record_inputs,
)

PRODUCER_NAME = "text_repeated_span"
PRODUCER_VERSION = "1"

# The window of block lengths the detector will accept as a repeat.
#
# Measured, not assumed. Across 835 repeated blocks in a deterministic 250-section
# CFR sample every one fell in 399-401 (82% exactly 400); across the full-corpus
# audit run the distribution was 400: 215,858, 399: 42,174, 398: 314, 397: 3,
# 396: 3, 395: 2. The window is widened to 402 on the top end because a detector
# whose ceiling equals the mode cannot observe anything above it -- an audit that
# searched 390-400 reported a maximum of 400 by construction, while an independent
# diff-based measurement on the same corpus found 401s.
#
# The floor is what keeps this honest. 395 characters of *exact* repetition
# immediately across a separator does not occur in drafted legal prose; lowering it
# toward ordinary phrase length would start flagging genuine repetition, and
# repeated legal language is real. Both bounds are folded into ``config_hash``, so
# changing either yields different artifact ids rather than silently restating a
# different conclusion under the old one.
MIN_REPEAT_LENGTH = 395
MAX_REPEAT_LENGTH = 402

# The separator the two copies sit across. A newline is what the observed defect
# leaves behind; requiring one (rather than scanning every offset) is both far
# cheaper and much stricter than a general longest-repeated-substring search.
_SEPARATOR = "\n"


class TextIntegrityRecord(Protocol):
    @property
    def source_record_id(self) -> str: ...

    @property
    def raw_text(self) -> str | None: ...


class TextIntegrityFlag(StrEnum):
    """Within-record integrity observations. One member today; the type exists so
    later within-record checks (truncation, embedded banners) extend the same
    annotation instead of inventing parallel artifacts."""

    REPEATED_SPAN = "repeated_span"


@dataclass(frozen=True, slots=True)
class RepeatedSpan:
    """One block of text observed twice, back to back, across a separator.

    Offsets are half-open and index the **raw** text of the record exactly as
    stored, so a consumer can verify the claim without re-running the detector:
    ``raw[first_start:first_start + length] == raw[second_start:second_start + length]``.

    Recording both copies rather than a removal interval is deliberate. Which copy
    to drop is a repair decision that belongs to a separate producer with its own
    evidence; this artifact states only what was observed.
    """

    first_start: int
    second_start: int
    length: int

    def __post_init__(self) -> None:
        if self.length <= 0:
            raise ValueError(f"RepeatedSpan.length must be positive, got {self.length}")
        if self.first_start < 0 or self.second_start < 0:
            raise ValueError("RepeatedSpan offsets must be non-negative")
        if self.first_start + self.length > self.second_start:
            raise ValueError(
                "a RepeatedSpan's two copies must not overlap "
                f"(first [{self.first_start}, {self.first_start + self.length}) "
                f"vs second start {self.second_start})"
            )

    @property
    def first_end(self) -> int:
        return self.first_start + self.length

    @property
    def second_end(self) -> int:
        return self.second_start + self.length


def detect_repeated_spans(
    text: str | None,
    *,
    min_length: int = MIN_REPEAT_LENGTH,
    max_length: int = MAX_REPEAT_LENGTH,
) -> tuple[RepeatedSpan, ...]:
    """Find blocks repeated immediately across a separator, left to right.

    At each separator, the **longest** qualifying block wins, and the scan resumes
    after the second copy. The *redundant* copies are therefore disjoint by
    construction and in ascending offset order, so no character is ever counted twice
    — a detector that emitted conflicting candidates would push a repair decision onto
    every consumer, and this producer does not make repair decisions. A block occurring
    three or more times chains: span 2's first copy is span 1's second, which is what
    that text actually looks like.

    Returns an empty tuple for null, short, or undamaged text.
    """
    if min_length <= 0 or max_length < min_length:
        raise ValueError(
            f"invalid repeat window: min_length={min_length}, max_length={max_length}"
        )
    if not text:
        return ()

    spans: list[RepeatedSpan] = []
    limit = len(text)
    cursor = 0
    while True:
        sep = text.find(_SEPARATOR, cursor)
        if sep < 0:
            break
        # Longest first: a shorter block would also match inside a longer repeat, and
        # reporting the short one would understate the observation.
        for length in range(max_length, min_length - 1, -1):
            first_start = sep - length
            second_start = sep + 1
            if first_start < 0 or second_start + length > limit:
                continue
            if text[first_start:sep] == text[second_start : second_start + length]:
                spans.append(RepeatedSpan(first_start, second_start, length))
                cursor = second_start + length
                break
        else:
            cursor = sep + 1
    return tuple(spans)


@dataclass(frozen=True, slots=True)
class TextIntegrityAnnotation:
    """One record's within-record integrity conclusion.

    Provenance names **exactly one** edge, this record. There is no scope artifact
    because the conclusion depends on no other row — which is the whole point of the
    separation from :class:`..quality.QualityAnnotation`, whose ``[scope, target]``
    contract exists to make a sibling-set change re-hash every conclusion.
    """

    provenance: DerivedArtifactProvenance
    target_source_record_id: str
    flags: tuple[TextIntegrityFlag, ...] = field(default_factory=tuple)
    repeated_spans: tuple[RepeatedSpan, ...] = field(default_factory=tuple)
    payload_hash: str = ""
    evidence: tuple[Evidence, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for i, flag in enumerate(self.flags):
            require_enum_member(flag, TextIntegrityFlag, f"flags[{i}]")
        if self.provenance.artifact_type != ArtifactType.TEXT_INTEGRITY_ANNOTATION:
            raise ValueError(
                f"TextIntegrityAnnotation provenance must be artifact_type "
                f"{ArtifactType.TEXT_INTEGRITY_ANNOTATION}, got "
                f"{self.provenance.artifact_type}"
            )
        if not self.target_source_record_id:
            raise ValueError("target_source_record_id must be non-empty")
        if self.provenance.source_record_ids() != (self.target_source_record_id,):
            raise ValueError(
                "TextIntegrityAnnotation provenance must name exactly its target as "
                f"the one source_record edge (target={self.target_source_record_id!r}, "
                f"edges={self.provenance.source_record_ids()})"
            )
        if len(self.provenance.inputs) != 1:
            raise ValueError(
                "TextIntegrityAnnotation provenance inputs must be exactly [target]; "
                f"this conclusion depends on no other artifact, got "
                f"{self.provenance.inputs}"
            )
        # The flag and the spans must agree, in both directions: a flag with nothing
        # to point at is an unsupported claim, and spans without the flag would hide a
        # finding from every consumer that reads flags.
        flagged = TextIntegrityFlag.REPEATED_SPAN in self.flags
        if flagged != bool(self.repeated_spans):
            raise ValueError(
                "repeated_span flag and repeated_spans must agree "
                f"(flag={flagged}, spans={len(self.repeated_spans)})"
            )
        starts = [s.second_start for s in self.repeated_spans]
        if starts != sorted(starts):
            raise ValueError("repeated_spans must be in ascending offset order")
        # Non-overlap is required of the SECOND copies, which are the redundant ones.
        # A later span's *first* copy may legitimately be an earlier span's second: that
        # is exactly what a block appearing three or more times looks like, and
        # forbidding it would reject real input rather than catch a defect.
        for earlier, later in zip(self.repeated_spans, self.repeated_spans[1:]):
            if later.second_start < earlier.second_end:
                raise ValueError(
                    "the redundant copies of two repeated_spans must not overlap; "
                    "the same characters would be counted twice "
                    f"({earlier} then {later})"
                )
        assign_payload_hash(
            self,
            ArtifactType.TEXT_INTEGRITY_ANNOTATION,
            {
                "target_source_record_id": self.target_source_record_id,
                "flags": list(self.flags),
                "repeated_spans": [
                    [s.first_start, s.second_start, s.length] for s in self.repeated_spans
                ],
                "evidence": list(self.evidence),
            },
        )

    @property
    def repeated_character_count(self) -> int:
        """Characters this row states redundantly — the size of the observation, not a
        claim about how many would survive a repair. A block occurring N times yields
        N-1 spans, so this counts the N-1 surplus copies, not all N."""
        return sum(span.length for span in self.repeated_spans)


def has_repeated_span(annotation: TextIntegrityAnnotation) -> bool:
    """The intended consumer read: the finding lives in ``flags``."""
    return TextIntegrityFlag.REPEATED_SPAN in annotation.flags


def _config_hash(min_length: int, max_length: int) -> str:
    # The detector window changes the conclusion, so it is derivation config. Without
    # this, re-running with a different window would restate a different result under
    # an unchanged artifact_id.
    return hashlib.sha256(
        f"{_SEPARATOR!r}\x00{min_length}\x00{max_length}".encode("utf-8")
    ).hexdigest()


def annotate_text_integrity(
    record: TextIntegrityRecord,
    *,
    min_length: int = MIN_REPEAT_LENGTH,
    max_length: int = MAX_REPEAT_LENGTH,
) -> TextIntegrityAnnotation:
    """Annotate one record with what its own bytes show.

    Needs no oracle, no identity group, and no siblings — which is what lets it run
    over corpora COV-1A cannot measure. A null body yields a flagless annotation:
    absent text is not clean text, and this producer certifies nothing about it.
    """
    source_record_id = record.source_record_id
    if not source_record_id:
        raise ValueError("record.source_record_id must be non-empty")
    raw_text = record.raw_text
    spans = detect_repeated_spans(raw_text, min_length=min_length, max_length=max_length)

    if raw_text is None:
        evidence: tuple[Evidence, ...] = (
            Evidence(
                "null_source_body",
                "record has no text; no within-record integrity claim is made",
                confidence=1.0,
            ),
        )
    elif spans:
        evidence = (
            Evidence(
                "repeated_span_exact",
                f"{len(spans)} block(s) of {min(s.length for s in spans)}-"
                f"{max(s.length for s in spans)} characters occur twice, back to back "
                f"across a separator, totalling "
                f"{sum(s.length for s in spans)} repeated characters",
                confidence=1.0,
            ),
        )
    else:
        evidence = (
            Evidence(
                "no_repeated_span",
                f"no exact block of {min_length}-{max_length} characters repeats "
                f"across a separator; this makes no claim about the rest of the text",
                confidence=1.0,
            ),
        )

    provenance = DerivedArtifactProvenance.build(
        ArtifactType.TEXT_INTEGRITY_ANNOTATION,
        source_record_inputs((source_record_id,)),
        PRODUCER_NAME,
        PRODUCER_VERSION,
        config_hash=_config_hash(min_length, max_length),
    )
    return TextIntegrityAnnotation(
        provenance=provenance,
        target_source_record_id=source_record_id,
        flags=(TextIntegrityFlag.REPEATED_SPAN,) if spans else (),
        repeated_spans=spans,
        evidence=evidence,
    )


def annotate_many(
    records: Iterable[TextIntegrityRecord],
    *,
    min_length: int = MIN_REPEAT_LENGTH,
    max_length: int = MAX_REPEAT_LENGTH,
) -> tuple[TextIntegrityAnnotation, ...]:
    """Annotate a stream of records. Each conclusion is independent, so this is a
    convenience over :func:`annotate_text_integrity` and imposes no scope."""
    return tuple(
        annotate_text_integrity(record, min_length=min_length, max_length=max_length)
        for record in records
    )
