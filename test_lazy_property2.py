# test_lazy_property2.py
import math
import pytest
from lazy_property import LazyProperty2, Circle


def test_area_computed_once(capsys):
    c = Circle(2)

    # First access → computation
    a1 = c.area
    captured1 = capsys.readouterr().out
    assert "computing area" in captured1

    # Second access → cached
    a2 = c.area
    captured2 = capsys.readouterr().out
    assert captured2 == ""  # no recomputation

    assert a1 == a2


def test_circumference_computed_once(capsys):
    c = Circle(3)

    _ = c.circumference
    captured1 = capsys.readouterr().out
    assert "computing circumference" in captured1

    _ = c.circumference
    captured2 = capsys.readouterr().out
    assert captured2 == ""


def test_correct_values():
    c = Circle(1)

    assert pytest.approx(c.area) == math.pi
    assert pytest.approx(c.circumference) == 2 * math.pi


def test_cached_in_instance_dict():
    c = Circle(4)

    _ = c.area
    assert "area" in c.__dict__

    _ = c.circumference
    assert "circumference" in c.__dict__


def test_instances_are_independent():
    c1 = Circle(2)
    c2 = Circle(3)

    assert c1.area != c2.area


def test_descriptor_access_via_class():
    # Access through class returns descriptor itself
    assert isinstance(Circle.area, LazyProperty2)
    assert isinstance(Circle.circumference, LazyProperty2)


def test_manual_cache_invalidation(capsys):
    c = Circle(2)

    _ = c.area
    capsys.readouterr()

    # Invalidate cache
    del c.__dict__["area"]

    _ = c.area
    captured = capsys.readouterr().out

    assert "computing area" in captured


def test_mutating_radius_does_not_recompute_automatically():
    c = Circle(2)
    a1 = c.area

    # Change underlying data
    c._radius = 10

    # Still cached → unchanged
    a2 = c.area

    assert a1 == a2  # demonstrates caching behavior


def test_recompute_after_radius_change_and_cache_clear():
    c = Circle(2)
    _ = c.area

    c._radius = 10
    del c.__dict__["area"]

    assert pytest.approx(c.area) == math.pi * 100
