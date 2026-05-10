"""Test fixtures for the resize script."""

from __future__ import annotations

import importlib.util
import pathlib
from types import ModuleType

import pytest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "python code to rezise it.py"


@pytest.fixture(scope="session")
def script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("resize_script", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
