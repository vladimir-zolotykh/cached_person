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
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = tuple((cls, *args))
        # if (obj := type(cls)._instances.get(cls)) is not None:
        #     return obj
        if (obj := type(cls)._instances.get(key)) is not None:
            return obj
        obj = super().__call__(*args, **kwargs)
        # type(cls)._instances[cls] = obj
        type(cls)._instances[key] = obj
        return obj


class Spam(metaclass=Singleton):
    def __init__(self):
        print("Initializing Spam")


class NoSpam(metaclass=CachedInstance):
    def __init__(self, x, y):
        print("Initializing NoSpam")


if __name__ == "__main__":
    s1 = Spam()
    s2 = Spam()
    assert s1 is s2
    n1 = NoSpam(20, 40)
    n2 = NoSpam(21, 42)
    print(id(n1), id(n2))
