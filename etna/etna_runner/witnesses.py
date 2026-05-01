"""Concrete witnesses for the funcy ETNA workload.

Each ``witness_<snake>_case_<tag>`` is a no-arg function calling
``property_<snake>`` with frozen inputs. On the base tree every witness
returns PASS; with the corresponding patch reverse-applied, the witness
returns ``fail(...)``.
"""
from __future__ import annotations

from . import properties
from ._result import PropertyResult


def witness_walk_values_defaultdict_factory_case_basic() -> PropertyResult:
    return properties.property_walk_values_defaultdict_factory([(1, 10), (2, 20)])


def witness_flatten_follow_argument_case_nested() -> PropertyResult:
    return properties.property_flatten_follow_argument([1, 2, 3])


def witness_iffy_default_argument_case_falsy() -> PropertyResult:
    # 1-arg iffy with default=99; calling on 0 (falsy) must return 99,
    # not identity(0) = 0 as the bug does.
    return properties.property_iffy_default_argument((5, 99))


def witness_empty_on_iterators_case_basic() -> PropertyResult:
    return properties.property_empty_on_iterators([1, 2, 3])


def witness_partition_by_extended_mapper_case_basic() -> PropertyResult:
    return properties.property_partition_by_extended_mapper([0, 1, 2, 3])


def witness_where_nonexistent_keys_case_missing() -> PropertyResult:
    # First entry has key 0 → mapping {} (no 'a' key); bug raises KeyError.
    return properties.property_where_nonexistent_keys([(0, 5), (1, 5)])


def witness_cache_mixed_args_case_basic() -> PropertyResult:
    return properties.property_cache_mixed_args((1, 2))
