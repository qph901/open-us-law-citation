"""The Python and SQL definitions of an ``act_id`` namespace must agree.

They did not used to be the same rule. The DuckDB harnesses used
``regexp_extract(act_id, '^[A-Za-z]+', 0)`` -- the leading run of *letters* -- while
:func:`act_id_prefix` takes everything before the first underscore. Those two rules give
different answers for several plausible id shapes, and they happened to coincide on all
2,978,617 rows of v2026.08, so no report would have shown the divergence. A future snapshot
introducing an id like ``USC2_T5`` would have split M0.5A/M0.5A.1's namespace tables from
the identity strategies' routing, silently.

This is a *differential* test: it runs both implementations over the same inputs, so the
two cannot drift apart without a failure.
"""

from __future__ import annotations

import duckdb
import pytest

from open_us_law_citation.derived.identity_strategies import (
    ACT_ID_NAMESPACE_SQL,
    act_id_prefix,
)

# Real shapes from the snapshot, plus the shapes that separate the two rules.
_CASES = [
    "CFR_T17_P240_S240_10b_5",     # real: codified CFR
    "FR_PRORULE_2025-06180",       # real: Federal Register
    "USC_T42_C21_S1983",           # real: US Code
    "STATE_CA_ADMIN_T1",           # real: state administrative code
    "USC2_T5",                     # letters then a DIGIT before the underscore
    "123_ABC",                     # no leading letters at all
    "CFRT17",                      # no underscore
    "_LEADING",                    # empty first segment
    "",                            # empty id
    "CFR__DOUBLE",                 # consecutive underscores
    "cfr_lower_case",              # lowercase
    "CFR-DASH_T1",                 # a dash before the underscore
]


@pytest.fixture(scope="module")
def con():
    connection = duckdb.connect()
    yield connection
    connection.close()


def _sql_namespace(con, act_id: str) -> str:
    expr = ACT_ID_NAMESPACE_SQL.format(col="?")
    return con.execute(f"SELECT {expr}", [act_id]).fetchone()[0]


@pytest.mark.parametrize("act_id", _CASES)
def test_sql_and_python_namespaces_agree(con, act_id):
    assert _sql_namespace(con, act_id) == act_id_prefix(act_id)


def test_the_cases_that_separate_the_two_rules_are_actually_covered():
    """Guard the guard: if these ever stopped differing under the OLD regex rule, the test
    above would pass vacuously and prove nothing."""
    import re

    old_rule = lambda a: (re.match(r"^[A-Za-z]+", a or "") or [""])[0]  # noqa: E731
    separating = [a for a in _CASES if old_rule(a) != act_id_prefix(a)]
    assert set(separating) >= {"USC2_T5", "123_ABC", "CFRT17", "CFR-DASH_T1"}


def test_null_act_id_matches_pythons_empty_string(con):
    """Python coerces a null id to ''. Without COALESCE, SQL would yield NULL and group it
    as its own namespace. No null act_id exists at v2026.08, but the twin should agree
    everywhere, not merely in practice."""
    assert _sql_namespace(con, None) == act_id_prefix(None) == ""
