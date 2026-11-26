"""Tests for the Temperature class. Run with: python -m pytest -v test_temperature.py"""

import pytest

from temperature import Temperature


#  1. Initialization
def test_default_unit():
    assert Temperature(20).unit == "C"


def test_case_insensitive_unit():
    assert Temperature(20, "f").unit == "F"


def test_read_only_attributes():
    t = Temperature(20, "C")
    with pytest.raises(AttributeError):
        t.value = 30
    with pytest.raises(AttributeError):
        t.unit = "K"


#  2. Validation
def test_invalid_unit():
    with pytest.raises(ValueError):
        Temperature(10, "X")


def test_below_absolute_zero():
    with pytest.raises(ValueError):
        Temperature(-274, "C")
    with pytest.raises(ValueError):
        Temperature(-460, "F")
    with pytest.raises(ValueError):
        Temperature(-1, "K")


#  3. Conversions 
@pytest.mark.parametrize("c, f, k", [
    (-273.15, -459.67, 0.0),   # absolute zero
    (-40, -40, 233.15),        # Celsius-Fahrenheit crossover
    (0, 32, 273.15),           # freezing point of water
    (37, 98.6, 310.15),        # human body temperature
    (100, 212, 373.15),        # boiling point of water
])
def test_conversions(c, f, k):
    t = Temperature(c, "C")
    assert t.to_fahrenheit() == pytest.approx(f)
    assert t.to_kelvin() == pytest.approx(k)
    assert Temperature(f, "F").to_celsius() == pytest.approx(c)
    assert Temperature(k, "K").to_celsius() == pytest.approx(c)


# 4. Round-trip conversion 
def test_round_trip():
    original = Temperature(25, "C")
    back = original.convert_to("F").convert_to("K").convert_to("C")
    assert back == original


#  5. Cross-unit comparisons 
def test_cross_unit_equality():
    assert Temperature(0, "C") == Temperature(32, "F")


def test_cross_unit_ordering():
    assert Temperature(0, "C") < Temperature(274, "K")
    assert Temperature(50, "F") <= Temperature(10, "C")
    assert Temperature(100, "C") > Temperature(200, "F")
    assert Temperature(373.15, "K") >= Temperature(212, "F")


#  6. Formatting 
def test_str():
    assert str(Temperature(25, "C")) == "25.00 °C"


def test_repr():
    assert repr(Temperature(25, "C")) == "Temperature(25.0, 'C')"
