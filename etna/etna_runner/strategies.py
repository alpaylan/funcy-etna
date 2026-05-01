"""Hypothesis SearchStrategy builders for the funcy ETNA workload.

CrossHair-compatible: ``st.integers``, ``st.lists``, ``st.tuples``,
``st.booleans`` only. No custom ``@composite`` that branches on intermediate
state.
"""
from __future__ import annotations

from hypothesis import strategies as st

_INT = st.integers(min_value=-50, max_value=50)
_KEY = st.integers(min_value=0, max_value=10)


def strategy_walk_values_defaultdict_factory():
    return st.lists(
        st.tuples(_KEY, _INT),
        min_size=1, max_size=4, unique_by=lambda kv: kv[0],
    )


def strategy_flatten_follow_argument():
    return st.lists(_INT, min_size=1, max_size=6)


def strategy_iffy_default_argument():
    return st.tuples(_INT, st.integers(min_value=1, max_value=100))


def strategy_empty_on_iterators():
    return st.lists(_INT, max_size=6)


def strategy_partition_by_extended_mapper():
    return st.lists(_INT, min_size=1, max_size=8)


def strategy_where_nonexistent_keys():
    return st.lists(
        st.tuples(st.integers(min_value=0, max_value=1), _INT),
        min_size=1, max_size=5,
    )


def strategy_cache_mixed_args():
    return st.tuples(_INT, _INT)
