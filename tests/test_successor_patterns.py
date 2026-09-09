"""The two successor patterns are near-duplicates on purpose; this pins the difference.

`recon.SUCCESSOR_POINTER_RE` and `snapshot_diff.SUCCESSOR_RE` look like a copy-paste with a
divergent verb list, which invites someone to "unify" them. They answer different questions:

    recon      PRESENCE  -- "does this body carry a disposition pointer at all?", used as a
                           boolean across every lineage status, so its verb list is WIDER
    diff       EXTRACTION -- pulls the successor id from rows already filtered to the three
                           move statuses, so its verb list is NARROWER

The narrow set must stay a strict SUBSET of the wide one: if a move verb were added to the
extractor without adding it to the presence check, recon would report a body as carrying no
pointer while snapshot_diff extracted a successor from it. These harnesses are deliberately
independent (CLAUDE.md: neither imports the other), so a test is the only thing that can
hold the relationship.
"""

from __future__ import annotations

import re

import pytest

from open_us_law_citation.recon import SUCCESSOR_POINTER_RE
from open_us_law_citation.snapshot_diff import SUCCESSOR_RE

_VERBS = re.compile(r"\(([A-Za-z|]+)\)")


def _verbs(pattern: re.Pattern) -> set[str]:
    return {v.casefold() for v in _VERBS.search(pattern.pattern).group(1).split("|")}


def test_extractor_verbs_are_a_strict_subset_of_the_presence_verbs():
    wide, narrow = _verbs(SUCCESSOR_POINTER_RE), _verbs(SUCCESSOR_RE)
    assert narrow < wide, f"extractor verbs {narrow - wide} are missing from the presence check"
    assert narrow == {"renumbered", "transferred", "recodified"}
    assert wide - narrow == {"omitted", "repealed", "see"}


@pytest.mark.parametrize(
    "text",
    [
        "[§2010. Renumbered §321]",
        "Section was renumbered §321.",
        "Transferred §16132, and amended",
        "Recodified §1815a-1.",
    ],
)
def test_presence_check_fires_wherever_the_extractor_does(text):
    """The subset relation has to hold on real text, not just in the verb lists."""
    if SUCCESSOR_RE.search(text):
        assert SUCCESSOR_POINTER_RE.search(text)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("[§2010. Renumbered §321]", "321"),          # the real snapshot format
        ("Section was renumbered §321.", "321"),      # sentence-final period NOT captured
        ("Renumbered §1815a-1.", "1815a-1"),          # letter+hyphen id, period excluded
        ("Renumbered §321, and amended", "321"),
        ("Renumbered §§321", "321"),                  # doubled section sign
    ],
)
def test_successor_id_never_captures_sentence_punctuation(text, expected):
    """`[0-9A-Za-z.\\-]+` used to swallow a trailing period, yielding `321.` -- an id that
    resolves to nothing. Latent at v2026.08 (0 of 393 real extractions were affected,
    because the snapshot's format is bracket-terminated) but wrong."""
    match = SUCCESSOR_RE.search(text)
    assert match is not None and match.group(2) == expected


def test_the_extractor_does_not_fire_on_a_prose_cross_reference():
    """`See §1124` is a cross-reference, not a disposition. It is in the PRESENCE list on
    purpose (recon counts pointers of any kind) but must never yield a successor id."""
    assert SUCCESSOR_RE.search("See §1124") is None
    assert SUCCESSOR_POINTER_RE.search("See §1124") is not None
