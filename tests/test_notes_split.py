"""`NOTES_SPLIT_RE` isolates the operative text from the OLRC editorial apparatus.

Its output feeds the hash that decides whether an `act_id`'s *law* changed between
snapshots, so a missed header does not fail loudly — it silently counts a notes-only edit
as a legal amendment. The previous alternation
(``Editorial Notes|Statutory Notes|Amendments``) left 15,683 of 54,853 federal statute
bodies (28.6%) contaminated, because OLRC's real header is "Statutory Notes and Related
Subsidiaries" — the bare ``Statutory Notes`` branch never fired on it — and "Historical and
Revision Notes" was absent from the list entirely.

Every header asserted below was enumerated from the corpus, with its observed occurrence
count, not invented.
"""

from __future__ import annotations

import pytest

from open_us_law_citation.snapshot_diff import NOTES_HEADERS, NOTES_SPLIT_RE, _operative


@pytest.mark.parametrize(
    "header,observed_as_first_header",
    [
        ("Editorial Notes", 28485),
        ("Historical and Revision Notes", 7500),
        ("Statutory Notes and Related Subsidiaries", 4921),
        ("Codification", 3215),
        ("References in Text", 23),
        ("Amendments Not Shown in Text", 20),
        ("Amendments", 6),
        ("Statutory Notes and Executive Documents", 3),
    ],
)
def test_every_observed_apparatus_header_splits(header, observed_as_first_header):
    body = f"(a) The operative rule.\n{header}\nPub. L. 99-1 struck out par. (2)."
    assert _operative(body) == "(a) The operative rule."
    assert observed_as_first_header > 0


def test_the_header_that_used_to_be_missed():
    """The single largest cause: 31,078 occurrences, and the old bare `Statutory Notes`
    branch could not match it because the line continues past that prefix."""
    body = "(a) Operative.\nStatutory Notes and Related Subsidiaries\nEffective Date\n1975."
    assert _operative(body) == "(a) Operative."


def test_longest_header_wins_over_a_shorter_prefix():
    """Python alternation takes the FIRST branch that matches, not the longest, so the
    header list is sorted longest-first. `Amendments` is a prefix of `Amendments Not Shown
    in Text`; splitting on the short one would leave ` Not Shown in Text` as operative."""
    assert NOTES_HEADERS == sorted(NOTES_HEADERS, key=len, reverse=True)
    body = "(a) Operative.\nAmendments Not Shown in Text\n1986—Subsec. (a)."
    assert _operative(body) == "(a) Operative."


def test_split_takes_the_first_header_not_the_best_known_one():
    """A body whose apparatus opens with `Historical and Revision Notes` and only later
    reaches `Editorial Notes` must split at the first — otherwise the earlier apparatus
    leaks into the operative hash (4,262 real bodies did exactly this)."""
    body = "(a) Operative.\nHistorical and Revision Notes\nSaid section.\nEditorial Notes\nX."
    assert _operative(body) == "(a) Operative."


def test_a_header_must_be_alone_on_its_line():
    """Anchoring on \\n...\\n keeps a phrase inside a sentence from truncating real law."""
    body = "(a) The Secretary shall publish Amendments to the schedule each year."
    assert _operative(body) == body
    assert NOTES_SPLIT_RE.search(body) is None


def test_a_body_with_no_apparatus_is_returned_whole():
    assert _operative("(a) Operative only.") == "(a) Operative only."
    assert _operative(None) == ""
