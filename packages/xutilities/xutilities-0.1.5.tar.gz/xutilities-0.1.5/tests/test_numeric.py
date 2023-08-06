# coding=utf-8
""" Tests for number related utilities. """

import pytest

from xutilities.numeric import is_odd, is_even


@pytest.fixture
def even_numbers():
    """Provides sequence of even numbers."""
    return 0, 2, 4, 10, 102, 10000472, -2, -49026


@pytest.fixture
def odd_numbers():
    """Provides sequence of odd numbers."""
    return 1, 7, 23, 10481, -1, -173, 597104865


def test_is_odd(even_numbers, odd_numbers):
    for x in even_numbers:
        assert not is_odd(x)
    for x in odd_numbers:
        assert is_odd(x)


def test_is_even(even_numbers, odd_numbers):
    for x in odd_numbers:
        assert not is_even(x)
    for x in even_numbers:
        assert is_even(x)


def test_type_error():
    invalid_types = (1.2, -6.37, 'abc', [1, 2, 3], {'a': 2}, (1, 2, 3))
    for x in invalid_types:
        with pytest.raises(TypeError):
            assert not is_odd(x)  # noqa
