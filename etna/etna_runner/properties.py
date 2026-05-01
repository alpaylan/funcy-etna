"""Property functions for the funcy ETNA workload.

Each property is pure, total, deterministic, and returns ``PropertyResult``.
PascalCase property names in the manifest map to ``property_<snake>`` here.
"""
from __future__ import annotations

import re
from collections import defaultdict
from typing import List, Tuple

from funcy import (
    cache,
    empty,
    flatten,
    iffy,
    is_seqcont,
    lpartition_by,
    walk_values,
    where,
)

from ._result import DISCARD, PASS, PropertyResult, fail


# ---------------------------------------------------------------------------
# 1. WalkValuesDefaultdictFactory (walk_values_defaultdict_factory_c245b04_1)
# ---------------------------------------------------------------------------
def property_walk_values_defaultdict_factory(args: List[Tuple[int, int]]) -> PropertyResult:
    """``walk_values(f, defaultdict(None, payload))`` must produce a result
    whose ``default_factory`` is ``None`` (i.e. preserved from the input)
    and whose values are ``{k: f(v) for k, v in payload}``. The bug builds
    ``compose(mapper, None)`` as the factory; on missing-key lookup that
    raises ``TypeError``. The fix preserves the original ``None`` factory
    so missing-key lookup raises ``KeyError`` (defaultdict's standard
    behaviour when default_factory is None).
    """
    pairs = args
    payload = dict(pairs)
    if not payload:
        return DISCARD
    coll = defaultdict(None, payload)
    try:
        out = walk_values(lambda v: v + 1, coll)
    except TypeError as e:
        return fail(f"walk_values raised TypeError on defaultdict(None, ...): {e}")
    except Exception as e:
        return fail(f"walk_values raised {type(e).__name__}: {e}")
    expected = {k: v + 1 for k, v in payload.items()}
    if dict(out) != expected:
        return fail(f"walk_values(...) = {dict(out)!r}; expected {expected!r}")
    if out.default_factory is not None:
        return fail(
            f"walk_values(...) preserved a non-None default_factory "
            f"{out.default_factory!r}; expected None (the source factory)"
        )
    # Confirm missing-key lookup raises KeyError, not TypeError.
    missing = max(payload.keys()) + 999 if payload else 0
    try:
        out[missing]
    except KeyError:
        return PASS
    except TypeError as e:
        return fail(
            f"walk_values(...) missing-key lookup raised TypeError "
            f"(default_factory mis-wrapped as compose): {e}"
        )
    except Exception as e:
        return fail(f"walk_values(...) missing-key lookup raised "
                    f"{type(e).__name__}: {e}")
    return fail("walk_values(...) missing-key lookup did not raise")


# ---------------------------------------------------------------------------
# 2. FlattenFollowArgument (flatten_follow_argument_54ed07a_1)
# ---------------------------------------------------------------------------
class _Wrap:
    """Container that ``is_seqcont`` does NOT match, but a user-supplied
    ``follow=isinstance(_, _Wrap)`` does."""
    __slots__ = ("items",)
    def __init__(self, items):
        self.items = list(items)
    def __iter__(self):
        return iter(self.items)


def property_flatten_follow_argument(args: List[int]) -> PropertyResult:
    """``flatten(nested, follow=is_wrap)`` must descend recursively using
    the user-supplied ``follow``, not the default ``is_seqcont``. With a
    custom container type that ``is_seqcont`` does not match, the buggy
    recursion stops at depth 1 — leaving inner ``_Wrap`` instances in the
    output instead of unpacking them.
    """
    xs = args
    if len(xs) < 2:
        return DISCARD
    # Nest depth 3 in _Wrap: each level requires recursion to descend into.
    # The buggy recursion uses is_seqcont (which rejects _Wrap), so it
    # yields the depth-1 _Wrap as-is instead of unpacking deeper.
    deep = _Wrap([_Wrap([_Wrap([xs[0]])])])
    nested = _Wrap([deep] + list(xs[1:]))
    is_wrap = lambda v: isinstance(v, _Wrap)
    try:
        out = list(flatten(nested, follow=is_wrap))
    except RecursionError:
        return fail("flatten() recursed indefinitely with custom follow")
    except Exception as e:
        return fail(f"flatten raised {type(e).__name__}: {e}")
    if out != list(xs):
        return fail(
            f"flatten(<_Wrap>, follow=is_wrap) = {out!r}; expected {list(xs)!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# 3. IffyDefaultArgument (iffy_default_argument_77e4c5e_1)
# ---------------------------------------------------------------------------
def property_iffy_default_argument(args: Tuple[int, int]) -> PropertyResult:
    """In the 1-arg form ``iffy(pred, default=k)``, ``pred`` plays the role
    of action (recurses internally as ``iffy(bool, pred, k)``). Calling the
    returned function on a falsy ``v`` must return the user-supplied
    ``default`` ``k`` — not the original ``v`` (which the bug returns by
    falling back to ``identity``).
    """
    pred_threshold, default = args
    if default == 0:
        return DISCARD
    pred = lambda v: v >= pred_threshold
    f = iffy(pred, default=default)
    try:
        out = f(0)
    except Exception as e:
        return fail(f"iffy(pred, default={default!r})(0) raised "
                    f"{type(e).__name__}: {e}")
    if out != default:
        return fail(
            f"iffy(pred, default={default!r})(0) = {out!r}; "
            f"expected {default!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# 4. EmptyOnIterators (empty_iterators_4a5e9df_1)
# ---------------------------------------------------------------------------
def property_empty_on_iterators(args: List[int]) -> PropertyResult:
    """``empty(iter(xs))`` must return an empty iterator without raising.
    The bug calls ``iter()`` (no argument) which is a TypeError.
    """
    xs = args
    it = iter(xs)
    try:
        out = empty(it)
    except TypeError as e:
        return fail(f"empty(iter({xs!r})) raised TypeError: {e}")
    except Exception as e:
        return fail(f"empty(iter({xs!r})) raised {type(e).__name__}: {e}")
    materialized = list(out)
    if materialized != []:
        return fail(f"empty(iter({xs!r})) = {materialized!r}; expected []")
    return PASS


# ---------------------------------------------------------------------------
# 5. PartitionByExtendedMapper (partition_by_extended_mapper_7729f8d_1)
# ---------------------------------------------------------------------------
def property_partition_by_extended_mapper(args: List[int]) -> PropertyResult:
    """``lpartition_by('\\d', s)`` (regex extended mapper) must group
    consecutive items by what the regex matches — not collapse all matches
    into a single True bucket.
    """
    xs = args
    if not xs:
        return DISCARD
    digits = "".join(str((v % 3) + 1) for v in xs)
    s = "".join(c if (i % 3) else "x" for i, c in enumerate(digits))
    pat = re.compile(r"\d")
    try:
        actual = lpartition_by(r"\d", list(s))
    except Exception as e:
        return fail(f"lpartition_by('\\d', {s!r}) raised {type(e).__name__}: {e}")
    expected = []
    cur_key = object()
    for ch in s:
        m = pat.match(ch)
        key = m.group(0) if m else None
        if key == cur_key and expected:
            expected[-1].append(ch)
        else:
            expected.append([ch])
            cur_key = key
    if actual != expected:
        return fail(
            f"lpartition_by('\\d', {list(s)!r}) = {actual!r}; expected {expected!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# 6. WhereNonexistentKeys (where_nonexistent_keys_e068b64_1)
# ---------------------------------------------------------------------------
def property_where_nonexistent_keys(args: List[Tuple[int, int]]) -> PropertyResult:
    """``where`` must not raise when an input mapping is missing one of the
    cond keys; it must simply skip that mapping. Each input is built as a
    list of ``(key, value)`` pairs interpreted as 0 or 1 keys present.
    """
    pairs = args
    if not pairs:
        return DISCARD
    target_v = pairs[0][1]
    mappings = []
    for k, v in pairs:
        if k == 0:
            mappings.append({})
        else:
            mappings.append({"a": v})
    try:
        out = list(where(mappings, a=target_v))
    except KeyError as e:
        return fail(f"where(mappings, a={target_v!r}) raised KeyError: {e}")
    except Exception as e:
        return fail(f"where raised {type(e).__name__}: {e}")
    expected = [m for m in mappings if m.get("a", object()) == target_v]
    if out != expected:
        return fail(
            f"where({mappings!r}, a={target_v!r}) = {out!r}; expected {expected!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# 7. CacheMixedArgs (cache_mixed_args_592b6ea_1)
# ---------------------------------------------------------------------------
def property_cache_mixed_args(args: Tuple[int, int]) -> PropertyResult:
    """``@cache(timeout)`` must call the wrapped function with the original
    positional and keyword arguments, not with ``*key`` (where ``key``
    includes sorted-kwarg-pairs).
    """
    a, b = args

    @cache(timeout=60)
    def add(x, y):
        return x + y

    try:
        out = add(a, y=b)
    except TypeError as e:
        return fail(f"cache add(a, y=b) raised TypeError: {e}")
    except Exception as e:
        return fail(f"cache add raised {type(e).__name__}: {e}")
    expected = a + b
    if out != expected:
        return fail(
            f"cached add({a!r}, y={b!r}) = {out!r}; expected {expected!r}"
        )
    return PASS
