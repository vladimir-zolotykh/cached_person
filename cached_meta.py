#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if Singleton._instance is not None:
            return Singleton._instance
        cls = super().__call__(*args, **kwargs)
        Singleton._instance = cls
        return cls


class Spam(metaclass=Singleton):
    def __init__(self):
        print("Initializing Spam")


if __name__ == "__main__":
    s1 = Spam()
    s2 = Spam()
    assert s1 is s2
