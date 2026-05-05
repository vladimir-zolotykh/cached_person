#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


@pytest.mark.parametrize("n, res", zip(range(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]))
def test_fib(n, res):
    assert fib(n) == res
