"""Tests for the sample calc module."""

import pytest

from quality_testbed.calc import add, divide


def test_add() -> None:
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_divide() -> None:
    assert divide(6, 3) == 2


def test_divide_by_zero() -> None:
    with pytest.raises(ValueError):
        divide(1, 0)
