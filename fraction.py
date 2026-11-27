"""Fraction class with integer numerator and a strictly positive denominator."""

from math import gcd


class Fraction:

    def __init__(self, numerator: int, denominator: int = 1):
        # bool is a subclass of int, but True/False make no sense as fraction parts
        for part in (numerator, denominator):
            if not isinstance(part, int) or isinstance(part, bool):
                raise TypeError("Numerator and denominator must be integers.")
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")

        # Keep the denominator strictly positive by moving the sign to the numerator
        if denominator < 0:
            numerator, denominator = -numerator, -denominator

        # Store the fraction in lowest terms, e.g. 2/4 -> 1/2
        common = gcd(numerator, denominator)
        self._numerator = numerator // common
        self._denominator = denominator // common

    #  Read-only attributes
    @propertyjupyter
    def numerator(self) -> int:
        return self._numerator

    @property
    def denominator(self) -> int:
        return self._denominator

    @staticmethod
    def _as_fraction(other):
        """Turn an int into a Fraction; return None for unsupported types."""
        if isinstance(other, Fraction):
            return other
        if isinstance(other, int) and not isinstance(other, bool):
            return Fraction(other)
        return None

    # String representations
    def __repr__(self) -> str:
        return f"Fraction({self._numerator}, {self._denominator})"

    def __str__(self) -> str:
        if self._denominator == 1:
            return str(self._numerator)
        return f"{self._numerator}/{self._denominator}"

    # Comparisons (a/b ? c/d  <=>  a*d ? c*b, since b, d > 0)
    def __eq__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return (self._numerator == other._numerator
                and self._denominator == other._denominator)

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator < other._numerator * self._denominator

    def __le__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator <= other._numerator * self._denominator

    def __gt__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator > other._numerator * self._denominator

    def __ge__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator >= other._numerator * self._denominator

    # Hashing (equal fractions must have equal hashes, needed since __eq__ is defined)
    def __hash__(self) -> int:
        return hash((self._numerator, self._denominator))

    # Arithmetic
    def __add__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return Fraction(self._numerator * other._denominator + other._numerator * self._denominator,
                        self._denominator * other._denominator)

    def __radd__(self, other):  # int + Fraction
        return self.__add__(other)

    def __sub__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return Fraction(self._numerator * other._denominator - other._numerator * self._denominator,
                        self._denominator * other._denominator)

    def __rsub__(self, other):  # int - Fraction
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return other.__sub__(self)

    def __mul__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return Fraction(self._numerator * other._numerator,
                        self._denominator * other._denominator)

    def __rmul__(self, other):  # int * Fraction
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        if other._numerator == 0:
            raise ZeroDivisionError("Cannot divide by a zero fraction.")
        return Fraction(self._numerator * other._denominator,
                        self._denominator * other._numerator)

    def __rtruediv__(self, other):  # int / Fraction
        other = self._as_fraction(other)
        if other is None:
            return NotImplemented
        return other.__truediv__(self)

    # Unary operators and conversions
    def __neg__(self):
        return Fraction(-self._numerator, self._denominator)

    def __abs__(self):
        return Fraction(abs(self._numerator), self._denominator)

    def __float__(self) -> float:
        return self._numerator / self._denominator

    def __bool__(self) -> bool:
        return self._numerator != 0
