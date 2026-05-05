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


class LazyProperty:
    def __init__(self, func, arg):
        self._func = func
        self._arg = arg

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self._name in instance.__dict__:
            return instance.__dict__[self._name]
        else:
            val = self._func(self._arg)
            instance.__dict__[self._name] = val
            return val

    def __set__(self, instance, value):
        pass


class Math:
    fib = LazyProperty(fib, 8)


if __name__ == "__main__":
    m = Math()
    print(m.fib)
