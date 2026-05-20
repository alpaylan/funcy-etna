# funcy — ETNA Tasks

Total tasks: 14

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `cache_mixed_args_592b6ea_1` | hypothesis | `CacheMixedArgs` | `witness_cache_mixed_args_case_basic` |
| 002 | `cache_mixed_args_592b6ea_1` | crosshair | `CacheMixedArgs` | `witness_cache_mixed_args_case_basic` |
| 003 | `empty_iterators_4a5e9df_1` | hypothesis | `EmptyOnIterators` | `witness_empty_on_iterators_case_basic` |
| 004 | `empty_iterators_4a5e9df_1` | crosshair | `EmptyOnIterators` | `witness_empty_on_iterators_case_basic` |
| 005 | `flatten_follow_argument_54ed07a_1` | hypothesis | `FlattenFollowArgument` | `witness_flatten_follow_argument_case_nested` |
| 006 | `flatten_follow_argument_54ed07a_1` | crosshair | `FlattenFollowArgument` | `witness_flatten_follow_argument_case_nested` |
| 007 | `iffy_default_argument_77e4c5e_1` | hypothesis | `IffyDefaultArgument` | `witness_iffy_default_argument_case_falsy` |
| 008 | `iffy_default_argument_77e4c5e_1` | crosshair | `IffyDefaultArgument` | `witness_iffy_default_argument_case_falsy` |
| 009 | `partition_by_extended_mapper_7729f8d_1` | hypothesis | `PartitionByExtendedMapper` | `witness_partition_by_extended_mapper_case_basic` |
| 010 | `partition_by_extended_mapper_7729f8d_1` | crosshair | `PartitionByExtendedMapper` | `witness_partition_by_extended_mapper_case_basic` |
| 011 | `walk_values_defaultdict_factory_c245b04_1` | hypothesis | `WalkValuesDefaultdictFactory` | `witness_walk_values_defaultdict_factory_case_basic` |
| 012 | `walk_values_defaultdict_factory_c245b04_1` | crosshair | `WalkValuesDefaultdictFactory` | `witness_walk_values_defaultdict_factory_case_basic` |
| 013 | `where_nonexistent_keys_e068b64_1` | hypothesis | `WhereNonexistentKeys` | `witness_where_nonexistent_keys_case_missing` |
| 014 | `where_nonexistent_keys_e068b64_1` | crosshair | `WhereNonexistentKeys` | `witness_where_nonexistent_keys_case_missing` |

## Witness Catalog

- `witness_cache_mixed_args_case_basic` — add(1, y=2) under @cache — fix returns 3, bug raises TypeError
- `witness_empty_on_iterators_case_basic` — iter([1,2,3]) — fix returns iter([]), bug TypeError
- `witness_flatten_follow_argument_case_nested` — [[[[1,2,3]]]] with follow=is_list — fix flattens to [1,2,3], bug returns one-level-deep list
- `witness_iffy_default_argument_case_falsy` — iffy(pred, default=99); 1-arg form means pred plays as action and default=99 must be returned for falsy v=0 — fix returns 99, bug returns identity(0)=0
- `witness_partition_by_extended_mapper_case_basic` — regex \d on mixed string — fix produces multiple chunks, bug collapses by truthiness
- `witness_walk_values_defaultdict_factory_case_basic` — defaultdict(None, {1:10, 2:20}) — fix yields mapped values, bug TypeError
- `witness_where_nonexistent_keys_case_missing` — mappings = [{}, {'a': 5}], where(..., a=5) — fix returns [{'a':5}], bug KeyError
