# funcy — Injected Bugs

A fancy and practical functional toolset for Python — bug fixes mined from upstream history.

Total mutations: 7

## Bug Index

| # | Variant | Name | Location | Injection | Fix Commit |
|---|---------|------|----------|-----------|------------|
| 1 | `cache_mixed_args_592b6ea_1` | `cache_mixed_args` | `funcy/calc.py:55` | `patch` | `592b6eaa3b004885ed0f4f1cbde81ffef3d91c87` |
| 2 | `empty_iterators_4a5e9df_1` | `empty_iterators` | `funcy/colls.py:50` | `patch` | `4a5e9df9d65c1dc980a1aeb5f2e0f837eae689e4` |
| 3 | `flatten_follow_argument_54ed07a_1` | `flatten_follow_argument` | `funcy/seqs.py:186` | `patch` | `54ed07a6a52acad6f409a828f544c37ace003902` |
| 4 | `iffy_default_argument_77e4c5e_1` | `iffy_default_argument` | `funcy/funcs.py:98` | `patch` | `77e4c5ee4f25fbcd760232e11da6df9f9a128322` |
| 5 | `partition_by_extended_mapper_7729f8d_1` | `partition_by_extended_mapper` | `funcy/seqs.py:402` | `patch` | `7729f8da225742c3eb9c9ab5f939efa0e6e6aea6` |
| 6 | `walk_values_defaultdict_factory_c245b04_1` | `walk_values_defaultdict_factory` | `funcy/colls.py:36` | `patch` | `c245b042616a2a88c250884b318b06ea0113ca58` |
| 7 | `where_nonexistent_keys_e068b64_1` | `where_nonexistent_keys` | `funcy/colls.py:360` | `patch` | `e068b64005b0f3c432311a7584b82d4e08420a67` |

## Property Mapping

| Variant | Property | Witness(es) |
|---------|----------|-------------|
| `cache_mixed_args_592b6ea_1` | `CacheMixedArgs` | `witness_cache_mixed_args_case_basic` |
| `empty_iterators_4a5e9df_1` | `EmptyOnIterators` | `witness_empty_on_iterators_case_basic` |
| `flatten_follow_argument_54ed07a_1` | `FlattenFollowArgument` | `witness_flatten_follow_argument_case_nested` |
| `iffy_default_argument_77e4c5e_1` | `IffyDefaultArgument` | `witness_iffy_default_argument_case_falsy` |
| `partition_by_extended_mapper_7729f8d_1` | `PartitionByExtendedMapper` | `witness_partition_by_extended_mapper_case_basic` |
| `walk_values_defaultdict_factory_c245b04_1` | `WalkValuesDefaultdictFactory` | `witness_walk_values_defaultdict_factory_case_basic` |
| `where_nonexistent_keys_e068b64_1` | `WhereNonexistentKeys` | `witness_where_nonexistent_keys_case_missing` |

## Framework Coverage

| Property | proptest | quickcheck | crabcheck | hegel |
|----------|---------:|-----------:|----------:|------:|
| `CacheMixedArgs` | ✓ | ✓ | ✓ | ✓ |
| `EmptyOnIterators` | ✓ | ✓ | ✓ | ✓ |
| `FlattenFollowArgument` | ✓ | ✓ | ✓ | ✓ |
| `IffyDefaultArgument` | ✓ | ✓ | ✓ | ✓ |
| `PartitionByExtendedMapper` | ✓ | ✓ | ✓ | ✓ |
| `WalkValuesDefaultdictFactory` | ✓ | ✓ | ✓ | ✓ |
| `WhereNonexistentKeys` | ✓ | ✓ | ✓ | ✓ |

## Bug Details

### 1. cache_mixed_args

- **Variant**: `cache_mixed_args_592b6ea_1`
- **Location**: `funcy/calc.py:55` (inside `_memory_decorator`)
- **Property**: `CacheMixedArgs`
- **Witness(es)**:
  - `witness_cache_mixed_args_case_basic` — add(1, y=2) under @cache — fix returns 3, bug raises TypeError
- **Source**: [#60](https://github.com/Suor/funcy/issues/60), internal — Fix @cache with mixed positional and keywords args
  > On a cache miss with mixed positional and keyword arguments the wrapper called ``func(*key, **kwargs)`` where ``key = args + tuple(sorted(kwargs.items()))``. The unpacked ``key`` includes the keyword-pair tuples as positional arguments, doubling those values and corrupting the function call. The fix dispatches with ``func(*args, **kwargs)``.
- **Fix commit**: `592b6eaa3b004885ed0f4f1cbde81ffef3d91c87` — Fix @cache with mixed positional and keywords args
- **Invariant violated**: Calling a ``@cache(timeout)``-wrapped function with mixed positional and keyword arguments returns the same result as calling the unwrapped function with the same arguments.
- **How the mutation triggers**: The mutation reverts the call to ``func(*key, **kwargs)``. With a positional + kwarg call, ``key`` includes the sorted ``(name, value)`` pair, so the wrapped function receives extra positional arguments and either raises ``TypeError`` or silently returns the wrong result.

### 2. empty_iterators

- **Variant**: `empty_iterators_4a5e9df_1`
- **Location**: `funcy/colls.py:50` (inside `empty`)
- **Property**: `EmptyOnIterators`
- **Witness(es)**:
  - `witness_empty_on_iterators_case_basic` — iter([1,2,3]) — fix returns iter([]), bug TypeError
- **Source**: internal — Fix empty() on iterators
  > ``empty(coll)`` for an iterator funnelled through ``_factory(coll)()`` which returned ``iter`` (the constructor) and then attempted ``iter()`` with no arguments — which raises ``TypeError: iter expected at least 1 argument``. The fix special-cases ``Iterator`` to return ``iter([])``.
- **Fix commit**: `4a5e9df9d65c1dc980a1aeb5f2e0f837eae689e4` — Fix empty() on iterators
- **Invariant violated**: ``list(empty(iter(xs)))`` is ``[]`` and the call does not raise.
- **How the mutation triggers**: The mutation removes the iterator special case so ``empty(iter(xs))`` falls into ``_factory(coll)()`` which is ``iter()``, raising ``TypeError``.

### 3. flatten_follow_argument

- **Variant**: `flatten_follow_argument_54ed07a_1`
- **Location**: `funcy/seqs.py:186` (inside `flatten`)
- **Property**: `FlattenFollowArgument`
- **Witness(es)**:
  - `witness_flatten_follow_argument_case_nested` — [[[[1,2,3]]]] with follow=is_list — fix flattens to [1,2,3], bug returns one-level-deep list
- **Source**: internal — Fix bug with flatten() follow argument
  > ``flatten(seq, follow=p)`` recursed with the default ``is_seqcont`` predicate instead of the user-supplied ``follow``. As a result, only the top-level was flattened with ``p``; deeper nestings were either over-unpacked (when ``p`` was narrower than ``is_seqcont``) or under-unpacked (when ``p`` accepted shapes ``is_seqcont`` rejects). The fix passes ``follow`` through every recursive call.
- **Fix commit**: `54ed07a6a52acad6f409a828f544c37ace003902` — Fix bug with flatten() follow argument
- **Invariant violated**: ``flatten(nested, follow=is_list)`` fully unpacks an arbitrary-depth list-of-lists when ``is_list`` is the user-supplied predicate.
- **How the mutation triggers**: The mutation reverts the recursive call to ``flatten(item, is_seqcont)``. ``is_seqcont`` does not consider plain ``list`` instances as sequence containers in some intermediate branches when other follow predicates are used; with the bug, the user's predicate is honoured only at depth 1.

### 4. iffy_default_argument

- **Variant**: `iffy_default_argument_77e4c5e_1`
- **Location**: `funcy/funcs.py:98` (inside `iffy`)
- **Property**: `IffyDefaultArgument`
- **Witness(es)**:
  - `witness_iffy_default_argument_case_falsy` — iffy(pred, default=99); 1-arg form means pred plays as action and default=99 must be returned for falsy v=0 — fix returns 99, bug returns identity(0)=0
- **Source**: internal — Fix iffy() default argument
  > ``iffy(pred, action=EMPTY, default=identity)`` recurses through the action-is-EMPTY branch as ``iffy(bool, pred)``, dropping any caller-supplied ``default`` and silently substituting ``identity``. The fix forwards ``default`` into the recursive call.
- **Fix commit**: `77e4c5ee4f25fbcd760232e11da6df9f9a128322` — Fix iffy() default argument
- **Invariant violated**: ``iffy(pred, default=k)(v)`` returns ``k`` when ``not pred(v)``.
- **How the mutation triggers**: The mutation drops the ``default`` argument from the recursive call, so the 1-arg form silently uses ``identity`` and the value passes through unchanged when it should fall back to ``k``.

### 5. partition_by_extended_mapper

- **Variant**: `partition_by_extended_mapper_7729f8d_1`
- **Location**: `funcy/seqs.py:402` (inside `partition_by`)
- **Property**: `PartitionByExtendedMapper`
- **Witness(es)**:
  - `witness_partition_by_extended_mapper_case_basic` — regex \d on mixed string — fix produces multiple chunks, bug collapses by truthiness
- **Source**: internal — Fix i?partition_by() for non-boolean extended mapper
  > ``partition_by(f, seq)`` forced the key function through ``make_pred`` rather than ``make_func``. ``make_pred`` wraps the result in ``bool``, collapsing every distinct match value into ``True`` and every miss into ``False``. With a regex string mapper like ``\d``, every digit collapses into one bucket instead of being grouped by the matched character.
- **Fix commit**: `7729f8da225742c3eb9c9ab5f939efa0e6e6aea6` — Fix i?partition_by() for non-boolean extended mapper
- **Invariant violated**: ``lpartition_by('\d', list(s))`` groups consecutive items by what the regex matches, distinguishing different match results — not by truthiness.
- **How the mutation triggers**: The mutation reverts to ``make_pred(f)``. The bool collapse erases distinctions between match values, so e.g. "1211" partitions into one chunk instead of three.

### 6. walk_values_defaultdict_factory

- **Variant**: `walk_values_defaultdict_factory_c245b04_1`
- **Location**: `funcy/colls.py:36` (inside `_factory`)
- **Property**: `WalkValuesDefaultdictFactory`
- **Witness(es)**:
  - `witness_walk_values_defaultdict_factory_case_basic` — defaultdict(None, {1:10, 2:20}) — fix yields mapped values, bug TypeError
- **Source**: internal — Fix walk_values() for defaultdicts with empty factory
  > ``_factory(coll, mapper=f)`` for a ``defaultdict`` with no ``default_factory`` (i.e. ``defaultdict(None, ...)``) constructed ``compose(mapper, None)`` whenever a mapper was supplied. ``compose`` returns a function that calls ``None()`` on first invocation, raising ``TypeError: 'NoneType' object is not callable`` from ``walk_values``. The fix only composes when ``coll.default_factory`` is itself truthy.
- **Fix commit**: `c245b042616a2a88c250884b318b06ea0113ca58` — Fix walk_values() for defaultdicts with empty factory
- **Invariant violated**: ``walk_values(f, defaultdict(None, payload))`` returns a defaultdict whose mapping equals ``{k: f(v) for k, v in payload}``, without raising.
- **How the mutation triggers**: The mutation drops the ``and coll.default_factory`` guard, so ``compose(mapper, None)`` is built and ``walk_values`` raises ``TypeError`` when the resulting factory is invoked.

### 7. where_nonexistent_keys

- **Variant**: `where_nonexistent_keys_e068b64_1`
- **Location**: `funcy/colls.py:360` (inside `where`)
- **Property**: `WhereNonexistentKeys`
- **Witness(es)**:
  - `witness_where_nonexistent_keys_case_missing` — mappings = [{}, {'a': 5}], where(..., a=5) — fix returns [{'a':5}], bug KeyError
- **Source**: internal — Don't crash in where on nonexistent keys from conditions
  > ``where(mappings, **cond)`` evaluated ``m[k] == v`` directly. If any mapping in ``mappings`` lacked a ``cond`` key, the call raised ``KeyError`` instead of treating the mapping as a non-match. The fix guards with ``k in m and m[k] == v``.
- **Fix commit**: `e068b64005b0f3c432311a7584b82d4e08420a67` — Don't crash in where on nonexistent keys from conditions
- **Invariant violated**: ``where(mappings, k=v)`` returns the mappings whose ``k`` equals ``v``; mappings lacking ``k`` are silently skipped, not surfaced as ``KeyError``.
- **How the mutation triggers**: The mutation drops the ``k in m`` guard from the lambda, so a mapping without one of the cond keys raises ``KeyError`` from inside ``filter``.
