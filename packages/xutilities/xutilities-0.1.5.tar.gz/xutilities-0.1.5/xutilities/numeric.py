# coding=utf-8
"""
Some utilities related to numbers.
"""


def is_even(num: int) -> bool:
    """Is num even?

    :param num: number to check.
    :type num: int
    :returns: True if num is even.
    :rtype: bool
    :raises: ``TypeError`` if num is not an int.
    """
    if not isinstance(num, int):
        raise TypeError("{} is not an int".format(num))
    return num % 2 == 0


def is_odd(num: int) -> bool:
    """Is num odd?

    :param num: number to check.
    :type num: int
    :returns: True if num is odd.
    :rtype: bool
    :raises: ``TypeError`` if num is not an int.
    """
    if not isinstance(num, int):
        raise TypeError("{} is not an int".format(num))
    return num % 2 == 1
