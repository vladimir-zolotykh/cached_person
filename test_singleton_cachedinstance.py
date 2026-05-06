# test_metaclasses.py

import pytest
from cached_meta import Singleton, CachedInstance


class Spam(metaclass=Singleton):
    def __init__(self):
        print("Initializing Spam")


class NoSpam(metaclass=CachedInstance):
    def __init__(self, x, y):
        print("Initializing NoSpam")


# --- fixtures to isolate global state ---


@pytest.fixture(autouse=True)
def clear_caches():
    Singleton._instances.clear()
    CachedInstance._instances.clear()
    yield


# --- tests for Singleton ---


def test_singleton_same_instance():
    s1 = Spam()
    s2 = Spam()

    assert s1 is s2


def test_singleton_init_called_once(capsys):
    _ = Spam()
    captured1 = capsys.readouterr().out
    assert "Initializing Spam" in captured1

    _ = Spam()
    captured2 = capsys.readouterr().out
    assert captured2 == ""  # no second initialization


def test_singleton_ignores_arguments():
    class A(metaclass=Singleton):
        def __init__(self, x):
            self.x = x

    a1 = A(10)
    a2 = A(20)

    assert a1 is a2
    assert a1.x == 10  # second call does not reinitialize


# --- tests for CachedInstance ---


def test_cached_instance_same_args_same_object():
    n1 = NoSpam(1, 2)
    n2 = NoSpam(1, 2)

    assert n1 is n2


def test_cached_instance_different_args_different_object():
    n1 = NoSpam(1, 2)
    n2 = NoSpam(2, 3)

    assert n1 is not n2


def test_cached_instance_init_called_per_unique_key(capsys):
    _ = NoSpam(1, 2)
    captured1 = capsys.readouterr().out
    assert "Initializing NoSpam" in captured1

    _ = NoSpam(1, 2)
    captured2 = capsys.readouterr().out
    assert captured2 == ""  # cached

    _ = NoSpam(2, 3)
    captured3 = capsys.readouterr().out
    assert "Initializing NoSpam" in captured3  # new key


def test_cached_instance_key_depends_only_on_args_not_kwargs():
    class B(metaclass=CachedInstance):
        def __init__(self, x=0):
            self.x = x

    b1 = B(x=1)
    b2 = B(x=1)

    # IMPORTANT: kwargs are ignored in your implementation → same key
    assert b1 is b2


def test_cached_instance_unhashable_args_fail():
    class C(metaclass=CachedInstance):
        def __init__(self, x):
            pass

    with pytest.raises(TypeError):
        C([1, 2, 3])  # list is unhashable → tuple key fails


# --- cross-class isolation ---


def test_different_classes_do_not_share_singleton():
    class A(metaclass=Singleton):
        pass

    class B(metaclass=Singleton):
        pass

    a = A()
    b = B()

    assert a is not b


def test_cached_instance_separates_classes():
    class A(metaclass=CachedInstance):
        def __init__(self, x):
            pass

    class B(metaclass=CachedInstance):
        def __init__(self, x):
            pass

    a = A(1)
    b = B(1)

    assert a is not b
