#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Person:
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, val):
        if not isinstance(val, int):
            raise TypeError(f"{val} must be of type int")
        self._age = val

    @age.deleter
    def age(self):
        raise AttributeError("Can't delete attribute")


class Subperson(Person):
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        print("Getting age")
        return super().age

    @age.setter
    def age(self, val):
        print("Setting age")
        super(Subperson, Subperson).age.__set__(self, val)

    @age.deleter
    def age(self):
        print("Deleting age")
        super(Subperson, Subperson).age.__delete__(self)


if __name__ == "__main__":
    p = Person(35)
    print(p.age)
    p.age = 36
    print(p.age)
    try:
        del p.age
    except AttributeError as e:
        print(e)
    print("*** Subperson")
    s = Subperson(35)
    print(s.age)
    s.age = 36
    print(s.age)
    try:
        del s.age
    except AttributeError as e:
        print(e)
