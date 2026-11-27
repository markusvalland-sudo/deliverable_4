"""Tests for the Fraction class. Run with: python -m pytest -v test_fraction.py"""

import pytest

from fraction import Fraction


#  1. Initialization
def test_default_denominator():
    f = Fraction(3)
    assert (f.numerator, f.denominator) == (3, 1)


def test_reduced_to_lowest_terms():
    f = Fraction(6, 8)
    assert (f.numerator, f.denominator) == (3, 4)


def test_negative_denominator_moves_sign():
    f = Fraction(1, -2)
    assert (f.numerator, f.denominator) == (-1, 2)
    g = Fraction(-1, -2)
    assert (g.numerator, g.denominator) == (1, 2)


def test_zero_numerator():
    f = Fraction(0, 5)
    assert (f.numerator, f.denominator) == (0, 1)


def test_read_only_attributes():
    f = Fraction(1, 2)
    with pytest.raises(AttributeError):
        f.numerator = 3
    with pytest.raises(AttributeError):
        f.denominator = 3


#  2. Validation
def test_zero_denominator():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 0)


@pytest.mark.parametrize("num, den", [(1.5, 2), (1, 2.0), ("1", 2), (True, 2)])
def test_non_integer_parts(num, den):
    with pytest.raises(TypeError):
        Fraction(num, den)


#  3. Comparisons
def test_equal():
    assert Fraction(1, 2) == Fraction(2, 4)
    assert Fraction(4, 2) == 2  # comparison with int


def test_not_equal():
    assert Fraction(1, 2) != Fraction(1, 3)
    assert Fraction(1, 2) != 1


def test_ordering():
    assert Fraction(1, 3) < Fraction(1, 2)
    assert Fraction(1, 2) <= Fraction(2, 4)
    assert Fraction(3, 4) > Fraction(2, 3)
    assert Fraction(2, 3) >= Fraction(4, 6)
    assert Fraction(-1, 2) < 0
    assert Fraction(5, 2) > 2


def test_compare_with_other_type():
    # == with an unsupported type falls back to identity, giving False
    assert (Fraction(1, 2) == "1/2") is False
    assert Fraction(1, 2).__eq__("1/2") is NotImplemented
    with pytest.raises(TypeError):
        Fraction(1, 2) < "1/2"


#  4. Arithmetic
def test_add():
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)
    assert Fraction(1, 2) + 1 == Fraction(3, 2)
    assert 1 + Fraction(1, 2) == Fraction(3, 2)


def test_sub():
    assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)
    assert 1 - Fraction(1, 4) == Fraction(3, 4)


def test_mul():
    assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)
    assert 3 * Fraction(1, 6) == Fraction(1, 2)


def test_truediv():
    assert Fraction(1, 2) / Fraction(1, 4) == 2
    assert 1 / Fraction(2, 3) == Fraction(3, 2)
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0, 1)


def test_unsupported_operand():
    with pytest.raises(TypeError):
        Fraction(1, 2) + 0.5


#  5. Unary operators and conversions
def test_neg_and_abs():
    assert -Fraction(1, 2) == Fraction(-1, 2)
    assert abs(Fraction(-3, 4)) == Fraction(3, 4)


def test_float():
    assert float(Fraction(1, 4)) == pytest.approx(0.25)


def test_bool():
    assert bool(Fraction(1, 2)) is True
    assert bool(Fraction(0, 3)) is False


def test_hash():
    assert hash(Fraction(1, 2)) == hash(Fraction(2, 4))
    assert len({Fraction(1, 2), Fraction(2, 4), Fraction(1, 3)}) == 2


#  6. Formatting
def test_str():
    assert str(Fraction(3, 4)) == "3/4"
    assert str(Fraction(4, 2)) == "2"


def test_repr():
    assert repr(Fraction(-2, 4)) == "Fraction(-1, 2)"
