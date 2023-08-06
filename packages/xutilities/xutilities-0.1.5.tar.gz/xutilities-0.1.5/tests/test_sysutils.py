#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `xutilities` package."""

from contextlib import contextmanager
from pathlib import Path

import pytest

from xutilities import sysutils


@contextmanager
def does_not_raise():
    """Dummy."""
    yield


@pytest.mark.parametrize(
    "executable, expectation",
    [
        ("python", does_not_raise()),
        (
            "unknown.exec",
            pytest.raises(
                sysutils.ExecutableNotFoundException,
                match="Executable not found in path: unknown.exec",
            ),
        ),
    ],
)
def test_which(executable, expectation):
    """Test which for specified executables."""
    with expectation:
        path_found = sysutils.which(executable)
        assert isinstance(path_found, Path)


def test_get_venv():
    """Test detection of virtual environment."""
    try:
        path_found = sysutils.get_venv()
    except sysutils.NoVirtualEnvironmentException as e:
        print(e)
        if e.path is not None:
            print("Directory listing:")
            print("-" * 40)
            for item in e.path.glob("*"):
                print(item)
            print("-" * 40)
        raise e
    assert isinstance(path_found, Path)
