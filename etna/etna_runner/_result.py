"""Framework-neutral PropertyResult, mirroring the Rust pipeline.

Pure data; no behavior. Property functions return one of PASS / DISCARD /
fail("reason"). The runner translates these into the JSON-on-stdout
contract described in etna-ify/prompts/run-python.md.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PropertyResult:
    kind: str           # "pass" | "fail" | "discard"
    message: str = ""

    @property
    def is_pass(self) -> bool: return self.kind == "pass"

    @property
    def is_fail(self) -> bool: return self.kind == "fail"


PASS = PropertyResult("pass")
DISCARD = PropertyResult("discard")


def fail(msg: str) -> PropertyResult:
    return PropertyResult("fail", msg)
