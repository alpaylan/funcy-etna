"""ETNA runner for Python workloads.

Dispatches `<tool> <property>` programmatically. Emits a single JSON line
on stdout per invocation; always exits 0 except on argv-parse errors.

Tools:
  * etna       — replays every witness for the property.
  * hypothesis — Hypothesis default backend (random + shrinking).
  * crosshair  — Hypothesis with backend="crosshair" (symbolic).
"""
from __future__ import annotations

import argparse
import json
import sys
import time

from hypothesis import HealthCheck, given, settings
from hypothesis.errors import HypothesisException

from . import properties, strategies, witnesses

ALL_PROPERTIES = [
    "WalkValuesDefaultdictFactory",
    "FlattenFollowArgument",
    "IffyDefaultArgument",
    "EmptyOnIterators",
    "PartitionByExtendedMapper",
    "WhereNonexistentKeys",
    "CacheMixedArgs",
]


def _pascal_to_snake(s: str) -> str:
    out = []
    for i, c in enumerate(s):
        if c.isupper() and i and not s[i - 1].isupper():
            out.append("_")
        out.append(c.lower())
    return "".join(out)


def _emit(tool: str, prop: str, status: str, tests: int, time_us: int,
          counterexample: str | None = None, error: str | None = None) -> None:
    sys.stdout.write(json.dumps({
        "status": status, "tests": tests, "discards": 0,
        "time": f"{time_us}us",
        "counterexample": counterexample, "error": error,
        "tool": tool, "property": prop,
    }) + "\n")
    sys.stdout.flush()


def _run_witness(prop: str) -> tuple[str, int, str | None]:
    snake = _pascal_to_snake(prop)
    fns = [getattr(witnesses, n) for n in dir(witnesses)
           if n.startswith(f"witness_{snake}_case_") and callable(getattr(witnesses, n))]
    if not fns:
        return ("aborted", 0, f"no witnesses for {prop}")
    for fn in fns:
        r = fn()
        if r.is_fail:
            return ("failed", 1, r.message)
    return ("passed", len(fns), None)


def _run_hypothesis(prop: str, backend: str, max_examples: int) -> tuple[str, int, str | None, str | None]:
    snake = _pascal_to_snake(prop)
    strat_fn = getattr(strategies, f"strategy_{snake}", None)
    prop_fn = getattr(properties, f"property_{snake}", None)
    if strat_fn is None or prop_fn is None:
        return ("aborted", 0, None, f"missing strategy or property for {prop}")
    counter = {"n": 0}
    counterexample: list[str | None] = [None]

    def _wrapped(args):
        counter["n"] += 1
        r = prop_fn(args)
        if r.is_fail:
            counterexample[0] = repr(args)
            assert False, r.message

    test = given(strat_fn())(_wrapped)
    test = settings(
        backend=backend,
        max_examples=max_examples,
        deadline=None,
        derandomize=False,
        suppress_health_check=list(HealthCheck),
        database=None,
    )(test)

    try:
        test()
        return ("passed", counter["n"], None, None)
    except AssertionError:
        return ("failed", counter["n"], counterexample[0] or "<unknown>", None)
    except HypothesisException as e:
        return ("failed", counter["n"], counterexample[0] or "<unknown>", str(e))
    except Exception as e:
        return ("failed", counter["n"], counterexample[0] or "<unknown>",
                f"{type(e).__name__}: {e}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("tool", choices=["etna", "hypothesis", "crosshair"])
    p.add_argument("property")
    p.add_argument("--max-examples", type=int, default=200)
    args = p.parse_args(argv)

    targets = ALL_PROPERTIES if args.property == "All" else [args.property]
    t0 = time.perf_counter()

    for prop in targets:
        if prop not in ALL_PROPERTIES:
            _emit(args.tool, prop, "aborted", 0, 0, None, f"unknown property: {prop}")
            continue
        if args.tool == "etna":
            status, tests, err = _run_witness(prop)
            cex = err if status == "failed" else None
            _emit(args.tool, prop, status, tests,
                  int((time.perf_counter() - t0) * 1e6), cex, None)
        else:
            backend = "crosshair" if args.tool == "crosshair" else "hypothesis"
            status, tests, cex, err = _run_hypothesis(prop, backend, args.max_examples)
            _emit(args.tool, prop, status, tests,
                  int((time.perf_counter() - t0) * 1e6), cex, err)

    return 0


if __name__ == "__main__":
    sys.exit(main())
