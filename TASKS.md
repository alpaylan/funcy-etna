# funcy — ETNA Tasks

Total tasks: 28

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `cache_mixed_args_592b6ea_1` | proptest | `CacheMixedArgs` | `witness_cache_mixed_args_case_basic` |
| 002 | `cache_mixed_args_592b6ea_1` | quickcheck | `CacheMixedArgs` | `witness_cache_mixed_args_case_basic` |
| 003 | `cache_mixed_args_592b6ea_1` | crabcheck | `CacheMixedArgs` | `witness_cache_mixed_args_case_basic` |
| 004 | `cache_mixed_args_592b6ea_1` | hegel | `CacheMixedArgs` | `witness_cache_mixed_args_case_basic` |
| 005 | `empty_iterators_4a5e9df_1` | proptest | `EmptyOnIterators` | `witness_empty_on_iterators_case_basic` |
| 006 | `empty_iterators_4a5e9df_1` | quickcheck | `EmptyOnIterators` | `witness_empty_on_iterators_case_basic` |
| 007 | `empty_iterators_4a5e9df_1` | crabcheck | `EmptyOnIterators` | `witness_empty_on_iterators_case_basic` |
| 008 | `empty_iterators_4a5e9df_1` | hegel | `EmptyOnIterators` | `witness_empty_on_iterators_case_basic` |
| 009 | `flatten_follow_argument_54ed07a_1` | proptest | `FlattenFollowArgument` | `witness_flatten_follow_argument_case_nested` |
| 010 | `flatten_follow_argument_54ed07a_1` | quickcheck | `FlattenFollowArgument` | `witness_flatten_follow_argument_case_nested` |
| 011 | `flatten_follow_argument_54ed07a_1` | crabcheck | `FlattenFollowArgument` | `witness_flatten_follow_argument_case_nested` |
| 012 | `flatten_follow_argument_54ed07a_1` | hegel | `FlattenFollowArgument` | `witness_flatten_follow_argument_case_nested` |
| 013 | `iffy_default_argument_77e4c5e_1` | proptest | `IffyDefaultArgument` | `witness_iffy_default_argument_case_falsy` |
| 014 | `iffy_default_argument_77e4c5e_1` | quickcheck | `IffyDefaultArgument` | `witness_iffy_default_argument_case_falsy` |
| 015 | `iffy_default_argument_77e4c5e_1` | crabcheck | `IffyDefaultArgument` | `witness_iffy_default_argument_case_falsy` |
| 016 | `iffy_default_argument_77e4c5e_1` | hegel | `IffyDefaultArgument` | `witness_iffy_default_argument_case_falsy` |
| 017 | `partition_by_extended_mapper_7729f8d_1` | proptest | `PartitionByExtendedMapper` | `witness_partition_by_extended_mapper_case_basic` |
| 018 | `partition_by_extended_mapper_7729f8d_1` | quickcheck | `PartitionByExtendedMapper` | `witness_partition_by_extended_mapper_case_basic` |
| 019 | `partition_by_extended_mapper_7729f8d_1` | crabcheck | `PartitionByExtendedMapper` | `witness_partition_by_extended_mapper_case_basic` |
| 020 | `partition_by_extended_mapper_7729f8d_1` | hegel | `PartitionByExtendedMapper` | `witness_partition_by_extended_mapper_case_basic` |
| 021 | `walk_values_defaultdict_factory_c245b04_1` | proptest | `WalkValuesDefaultdictFactory` | `witness_walk_values_defaultdict_factory_case_basic` |
| 022 | `walk_values_defaultdict_factory_c245b04_1` | quickcheck | `WalkValuesDefaultdictFactory` | `witness_walk_values_defaultdict_factory_case_basic` |
| 023 | `walk_values_defaultdict_factory_c245b04_1` | crabcheck | `WalkValuesDefaultdictFactory` | `witness_walk_values_defaultdict_factory_case_basic` |
| 024 | `walk_values_defaultdict_factory_c245b04_1` | hegel | `WalkValuesDefaultdictFactory` | `witness_walk_values_defaultdict_factory_case_basic` |
| 025 | `where_nonexistent_keys_e068b64_1` | proptest | `WhereNonexistentKeys` | `witness_where_nonexistent_keys_case_missing` |
| 026 | `where_nonexistent_keys_e068b64_1` | quickcheck | `WhereNonexistentKeys` | `witness_where_nonexistent_keys_case_missing` |
| 027 | `where_nonexistent_keys_e068b64_1` | crabcheck | `WhereNonexistentKeys` | `witness_where_nonexistent_keys_case_missing` |
| 028 | `where_nonexistent_keys_e068b64_1` | hegel | `WhereNonexistentKeys` | `witness_where_nonexistent_keys_case_missing` |

## Witness Catalog

- `witness_cache_mixed_args_case_basic` — add(1, y=2) under @cache — fix returns 3, bug raises TypeError
- `witness_empty_on_iterators_case_basic` — iter([1,2,3]) — fix returns iter([]), bug TypeError
- `witness_flatten_follow_argument_case_nested` — [[[[1,2,3]]]] with follow=is_list — fix flattens to [1,2,3], bug returns one-level-deep list
- `witness_iffy_default_argument_case_falsy` — iffy(pred, default=99); 1-arg form means pred plays as action and default=99 must be returned for falsy v=0 — fix returns 99, bug returns identity(0)=0
- `witness_partition_by_extended_mapper_case_basic` — regex \d on mixed string — fix produces multiple chunks, bug collapses by truthiness
- `witness_walk_values_defaultdict_factory_case_basic` — defaultdict(None, {1:10, 2:20}) — fix yields mapped values, bug TypeError
- `witness_where_nonexistent_keys_case_missing` — mappings = [{}, {'a': 5}], where(..., a=5) — fix returns [{'a':5}], bug KeyError
