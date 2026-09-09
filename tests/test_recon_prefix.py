"""`recon`'s act_id namespace SCHEME is deliberately not the identity strategies' prefix.

There are two legitimate notions of an act_id "namespace" in this repo, and a reader who
notices both is likely to assume one is a bug. This test records that they differ on
purpose, and would fail if someone made them agree:

    act_id_prefix        -> what an identity STRATEGY routes on   (CFR / FR / STATE)
    ACT_ID_SCHEME_REGEX  -> what the M0 report ENUMERATES         (USC / STATE_AK / SCONST_AK)

Collapsing the second into the first would merge every state into one row and destroy the
M0 finding it exists to show: a bare act_id is unique only within corpus+jurisdiction,
which is why uniqueness is enforced on `(state, corpus, act_id)`.
"""

from __future__ import annotations

import re

import pytest

from open_us_law_citation.derived.identity_strategies import act_id_prefix
from open_us_law_citation.recon import ACT_ID_SCHEME_REGEX

# Real act_id shapes named in recon's own comment, plus the federal ones.
_CASES = [
    ("USC_T10_C1001_S10001", "USC", "USC"),
    ("CFR_T17_P240_S240_10b_5", "CFR", "CFR"),
    ("FR_PRORULE_2025-06180", "FR", "FR"),
    ("STATE_AK_T10_C10.06_S10.06.005", "STATE_AK", "STATE"),
    ("SCONST_AK_A10_S0", "SCONST_AK", "SCONST"),
]


def _scheme(act_id: str) -> str | None:
    match = re.match(ACT_ID_SCHEME_REGEX, act_id)
    return match.group(1) if match else None


@pytest.mark.parametrize("act_id,expected_scheme,expected_prefix", _CASES)
def test_scheme_and_prefix_each_return_their_own_answer(
    act_id, expected_scheme, expected_prefix
):
    assert _scheme(act_id) == expected_scheme
    assert act_id_prefix(act_id) == expected_prefix


def test_the_two_notions_really_do_diverge_on_state_ids():
    """Guard the guard: if these ever agreed everywhere, the parametrised test above would
    still pass while the distinction it documents had quietly vanished."""
    diverging = [a for a, _, _ in _CASES if _scheme(a) != act_id_prefix(a)]
    assert set(diverging) == {"STATE_AK_T10_C10.06_S10.06.005", "SCONST_AK_A10_S0"}


def test_scheme_regex_requires_the_trailing_underscore():
    """It anchors on `PREFIX_`, so an id with no underscore has no scheme rather than a
    guessed one — abstention, not a fabricated namespace."""
    assert _scheme("USCT10") is None
    assert _scheme("") is None
    # A lowercase id does not match: the observed corpus uses uppercase schemes only.
    assert _scheme("usc_t10") is None
