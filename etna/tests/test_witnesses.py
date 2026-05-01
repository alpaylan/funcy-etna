"""Pytest collection for witnesses. Lets `pytest` exercise every witness as
a base-tree sanity check (every witness must return PropertyResult.is_pass on
HEAD). The runner uses the witnesses module directly via tool=etna.
"""
from __future__ import annotations

import pytest

from etna_runner import witnesses


def _all_witnesses():
    return [
        (name, getattr(witnesses, name))
        for name in dir(witnesses)
        if name.startswith("witness_") and callable(getattr(witnesses, name))
    ]


@pytest.mark.parametrize("name,fn", _all_witnesses())
def test_witness_passes_on_base(name, fn):
    r = fn()
    assert r.is_pass, f"{name}: {r.message}"
