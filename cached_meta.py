#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if type(cls)._instance is not None:
            return type(cls)._instance
        obj = super().__call__(*args, **kwargs)
        type(cls)._instance = obj
        return obj


class Spam(metaclass=Singleton):
    def __init__(self):
        print("Initializing Spam")


class NoSpam(metaclass=Singleton):
    def __init__(self):
        print("Initializing NoSpam")


if __name__ == "__main__":
    s1 = Spam()
    s2 = Spam()
    assert s1 is s2
    n1 = NoSpam()
    n2 = NoSpam()
    assert n1 is n2
