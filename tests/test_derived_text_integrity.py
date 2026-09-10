"""Golden-fixture suite for the within-record repeated-span detector.

The negative cases carry the weight here. This detector's output becomes a flag on
real law, so the expensive failure is not missing a defect — it is asserting that a
provision repeats itself when the drafter wrote it that way. Repeated legal language
is real, and every case below that must NOT fire is a shape that exists in the corpus.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import pytest

from open_us_law_citation.derived import (
    MAX_REPEAT_LENGTH,
    MIN_REPEAT_LENGTH,
    ArtifactInput,
    ArtifactType,
    DerivedArtifactProvenance,
    InputType,
    RepeatedSpan,
    TextIntegrityAnnotation,
    TextIntegrityFlag,
    annotate_many,
    annotate_text_integrity,
    check_payload_collisions,
    detect_repeated_spans,
    has_repeated_span,
)

RECORD_ID = "srr:sha256:" + "a" * 64
OTHER_ID = "srr:sha256:" + "b" * 64


@dataclass(frozen=True)
class _Record:
    source_record_id: str
    raw_text: str | None


def _block(seed: str, length: int) -> str:
    """Deterministic prose-shaped filler of an exact length."""
    unit = f"{seed} the Administrator shall publish a notice in the Federal Register. "
    return (unit * (length // len(unit) + 2))[:length]


def _damaged(length: int = 400, *, head: str = "(a) ", tail: str = " (b) After.") -> str:
    """A row with one block stated twice across a newline — the observed defect."""
    body = _block("alpha", length)
    return f"{head}{body}\n{body}{tail}"


# --- what must fire -----------------------------------------------------------------


@pytest.mark.parametrize("length", [MIN_REPEAT_LENGTH, 399, 400, 401, MAX_REPEAT_LENGTH])
def test_an_exact_block_repeated_across_a_newline_is_detected(length: int):
    text = _damaged(length)
    spans = detect_repeated_spans(text)
    assert len(spans) == 1
    span = spans[0]
    assert span.length == length
    # The offsets must be verifiable against the raw text without re-running us.
    assert text[span.first_start : span.first_end] == text[span.second_start : span.second_end]
    assert text[span.first_end] == "\n"


def test_several_repeats_in_one_row_are_all_reported_in_order():
    a, b, c = _block("alpha", 400), _block("bravo", 400), _block("charlie", 400)
    text = f"start {a}\n{a} middle {b}\n{b} then {c}\n{c} end"
    spans = detect_repeated_spans(text)
    assert len(spans) == 3
    assert [s.length for s in spans] == [400, 400, 400]
    assert [s.second_start for s in spans] == sorted(s.second_start for s in spans)
    for s in spans:
        assert text[s.first_start : s.first_end] == text[s.second_start : s.second_end]


def test_a_block_repeated_four_times_chains_without_double_counting():
    """Three or more copies is real input, and it is where a naive non-overlap rule
    breaks: span 2's first copy IS span 1's second copy. That must be allowed, while
    the redundant copies themselves stay disjoint so no character is counted twice."""
    unit = _block("delta", 400)
    text = f"{unit}\n{unit}\n{unit}\n{unit}"
    spans = detect_repeated_spans(text)
    assert len(spans) == 3                      # four copies -> three surplus
    for earlier, later in zip(spans, spans[1:]):
        assert later.second_start >= earlier.second_end
    # The producer must accept it rather than raise on its own detector's output.
    annotation = annotate_text_integrity(_Record(RECORD_ID, text))
    assert annotation.repeated_character_count == 1200


def test_the_longest_qualifying_block_wins():
    """A 402-char repeat also contains a 400-char repeat; reporting the short one
    would understate the observation."""
    body = _block("echo", MAX_REPEAT_LENGTH)
    spans = detect_repeated_spans(f"x {body}\n{body} y")
    assert len(spans) == 1 and spans[0].length == MAX_REPEAT_LENGTH


# --- what must NOT fire -------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "why"),
    [
        ("", "empty text"),
        ("   \n   ", "whitespace only"),
        ("(a) A short provision.\n(b) Another.", "far below the floor"),
        (_block("foxtrot", 4000), "long text, no repeat at all"),
    ],
)
def test_undamaged_text_yields_no_span(text: str, why: str):
    assert detect_repeated_spans(text) == (), why


def test_a_repeat_one_character_below_the_floor_does_not_fire():
    """The floor is the whole safety margin. A block just under it must not fire, or
    the window is not actually bounding anything."""
    body = _block("golf", MIN_REPEAT_LENGTH - 1)
    assert detect_repeated_spans(f"x {body}\n{body} y") == ()


def test_intentionally_repeated_legal_language_is_not_flagged():
    """Drafters restate definitions and parallel findings. Without a separator between
    two copies this is ordinary prose, and flagging it would call correct law damaged."""
    clause = _block("hotel", 420)
    # Repeated, but as running prose in one paragraph -- no separator between copies.
    assert detect_repeated_spans(f"(a) {clause} {clause}") == ()


def test_a_near_repeat_that_differs_by_one_character_does_not_fire():
    """Legal text differing by a number or a negation is the dangerous near-miss: the
    two copies say different things, and treating them as duplicates would delete law."""
    body = _block("india", 400)
    altered = body[:200] + ("9" if body[200] != "9" else "8") + body[201:]
    assert len(altered) == len(body)
    assert detect_repeated_spans(f"x {body}\n{altered} y") == ()


def test_a_repeat_separated_by_anything_other_than_the_separator_does_not_fire():
    body = _block("juliet", 400)
    assert detect_repeated_spans(f"x {body} {body} y") == ()      # a space
    assert detect_repeated_spans(f"x {body}; {body} y") == ()     # punctuation


def test_null_text_is_not_clean_text():
    assert detect_repeated_spans(None) == ()
    annotation = annotate_text_integrity(_Record(RECORD_ID, None))
    assert not has_repeated_span(annotation)
    assert annotation.repeated_spans == ()
    # ... and the annotation says why, rather than implying the row was checked clean.
    assert annotation.evidence[0].kind == "null_source_body"


# --- the annotation contract --------------------------------------------------------


def test_annotation_names_exactly_its_own_record_and_nothing_else():
    """The point of a separate type: this conclusion depends on no sibling, so it has
    no scope edge -- unlike QualityAnnotation, whose [scope, target] contract exists to
    make a sibling-set change re-hash every conclusion."""
    annotation = annotate_text_integrity(_Record(RECORD_ID, _damaged()))
    assert annotation.provenance.artifact_type == ArtifactType.TEXT_INTEGRITY_ANNOTATION
    assert annotation.provenance.source_record_ids() == (RECORD_ID,)
    assert len(annotation.provenance.inputs) == 1
    assert annotation.provenance.input_ids_of(InputType.ANNOTATION) == ()


def test_a_flagged_annotation_must_point_at_something():
    annotation = annotate_text_integrity(_Record(RECORD_ID, _damaged()))
    with pytest.raises(ValueError, match="must agree"):
        replace(annotation, repeated_spans=(), payload_hash="")
    clean = annotate_text_integrity(_Record(RECORD_ID, "(a) Short."))
    with pytest.raises(ValueError, match="must agree"):
        replace(clean, flags=(TextIntegrityFlag.REPEATED_SPAN,), payload_hash="")


def test_a_span_whose_copies_overlap_is_rejected():
    with pytest.raises(ValueError, match="must not overlap"):
        RepeatedSpan(first_start=0, second_start=100, length=400)
    with pytest.raises(ValueError, match="positive"):
        RepeatedSpan(first_start=0, second_start=500, length=0)


def test_provenance_cannot_be_borrowed_from_another_record():
    annotation = annotate_text_integrity(_Record(RECORD_ID, _damaged()))
    with pytest.raises(ValueError, match="exactly its target"):
        replace(annotation, target_source_record_id=OTHER_ID, payload_hash="")


def test_the_detector_window_is_derivation_config_not_a_silent_knob():
    """Changing the window changes the conclusion, so it must change the artifact id.
    If it did not, a rerun would restate a different result under the old address."""
    record = _Record(RECORD_ID, _damaged())
    default = annotate_text_integrity(record)
    widened = annotate_text_integrity(record, min_length=300, max_length=402)
    assert default.provenance.config_hash != widened.provenance.config_hash
    assert default.provenance.artifact_id != widened.provenance.artifact_id


def test_two_records_never_collide_and_the_tripwire_stays_silent():
    annotations = annotate_many(
        [_Record(RECORD_ID, _damaged()), _Record(OTHER_ID, _damaged())]
    )
    ids = {a.provenance.artifact_id for a in annotations}
    assert len(ids) == 2
    check_payload_collisions(annotations)


def test_identical_input_reproduces_an_identical_artifact():
    a = annotate_text_integrity(_Record(RECORD_ID, _damaged()))
    b = annotate_text_integrity(_Record(RECORD_ID, _damaged()))
    assert a.provenance.artifact_id == b.provenance.artifact_id
    assert a.payload_hash == b.payload_hash


def test_payload_hash_separates_a_flagged_row_from_a_clean_one():
    flagged = annotate_text_integrity(_Record(RECORD_ID, _damaged()))
    clean = annotate_text_integrity(_Record(RECORD_ID, "(a) A short provision."))
    # Same record, same producer, same config -> the derivation address is equal ...
    assert flagged.provenance.artifact_id == clean.provenance.artifact_id
    # ... so the semantic address is what must distinguish them, and the tripwire
    # must notice if both were ever stored.
    assert flagged.payload_hash != clean.payload_hash
    with pytest.raises(Exception):
        check_payload_collisions([flagged, clean])


def test_repeated_character_count_reports_the_observation_size():
    a, b = _block("kilo", 400), _block("lima", 399)
    annotation = annotate_text_integrity(_Record(RECORD_ID, f"x {a}\n{a} y {b}\n{b} z"))
    assert annotation.repeated_character_count == 799


def test_a_bad_window_is_refused_rather_than_silently_normalized():
    with pytest.raises(ValueError, match="invalid repeat window"):
        detect_repeated_spans("text", min_length=400, max_length=399)
    with pytest.raises(ValueError, match="invalid repeat window"):
        detect_repeated_spans("text", min_length=0, max_length=400)


def test_direct_construction_still_has_to_content_address_itself():
    provenance = DerivedArtifactProvenance.build(
        ArtifactType.TEXT_INTEGRITY_ANNOTATION,
        (ArtifactInput(InputType.SOURCE_RECORD, RECORD_ID),),
        "text_repeated_span",
        "1",
    )
    ok = TextIntegrityAnnotation(provenance=provenance, target_source_record_id=RECORD_ID)
    assert ok.payload_hash
    # An extra edge breaks the "depends on nothing else" contract.
    two_edges = DerivedArtifactProvenance.build(
        ArtifactType.TEXT_INTEGRITY_ANNOTATION,
        (
            ArtifactInput(InputType.SOURCE_RECORD, RECORD_ID),
            ArtifactInput(InputType.ANNOTATION, "scope:whatever"),
        ),
        "text_repeated_span",
        "1",
    )
    with pytest.raises(ValueError, match="exactly"):
        TextIntegrityAnnotation(
            provenance=two_edges, target_source_record_id=RECORD_ID
        )
