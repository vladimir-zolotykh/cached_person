#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if (obj := type(cls)._instances.get(cls)) is not None:
            return obj
        obj = super().__call__(*args, **kwargs)
        type(cls)._instances[cls] = obj
        return obj


class CachedInstance(type):
    pass


class Spam(metaclass=Singleton):
    def __init__(self, a, b):
        print("Initializing Spam")


class NoSpam(metaclass=Singleton):
    def __init__(self, x, y):
        print("Initializing NoSpam")


if __name__ == "__main__":
    s1 = Spam(10, 20)
    s2 = Spam(10, 20)
    assert s1 is s2
    n1 = NoSpam(20, 40)
    n2 = NoSpam(20, 40)
    assert n1 is n2
