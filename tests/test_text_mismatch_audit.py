"""Guards for the audit experiment; this is not a production repair producer."""

from scripts.audit_text_mismatch import propose_removals


def test_exact_overlap_removal_preserves_other_characters_and_raw_offsets():
    repeated = "".join(chr(0x100 + i) for i in range(400))
    raw = "Original prefix: " + repeated + "\n\n" + repeated + ". Tail stays."
    candidate, spans, conflict = propose_removals(raw)
    assert not conflict
    assert candidate == "Original prefix: " + repeated + ". Tail stays."
    start, end, size = spans[0]
    assert size == 400
    assert raw[start:end] == "\n\n" + repeated
    assert raw[:start] + raw[end:] == candidate


def test_similar_passages_and_short_repetitions_are_not_changed():
    repeated = "".join(chr(0x100 + i) for i in range(400))
    for raw in (
        repeated + "\n" + repeated[:200] + "Z" + repeated[201:],
        "Short but legally intentional.\nShort but legally intentional.",
        "Keep  spaces\nand punctuation—exactly.",
        "",
    ):
        assert propose_removals(raw) == (raw, [], False)


def test_conflicting_removal_intervals_abstain():
    raw = ("x" * 199 + "\n") * 8
    candidate, spans, conflict = propose_removals(raw)
    assert conflict and spans
    assert candidate == raw


def test_candidate_rule_cannot_certify_legitimate_repetition():
    # A real source can intentionally repeat 400 characters. This diagnostic
    # proposes an edit anyway: only a separate validation step can accept it.
    repeated = "".join(chr(0x100 + i) for i in range(400))
    official = repeated + "\n" + repeated
    candidate, spans, conflict = propose_removals(official)
    assert spans and not conflict
    assert candidate != official
