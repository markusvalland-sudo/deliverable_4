"""Temperature class supporting Celsius, Fahrenheit and Kelvin."""


class Temperature:
    """A temperature with a value and a unit ('C', 'F' or 'K')."""

    VALID_UNITS = ("C", "F", "K")
    TOL = 1e-9

    def __init__(self, value: float, unit: str = "C"):
        self._unit = self._validate_unit(unit)
        self._value = float(value)
        if self.to_kelvin() < -self.TOL:
            raise ValueError("Temperature cannot be below absolute zero (0 K).")

    @classmethod
    def _validate_unit(cls, unit: str) -> str:
        """Return the unit in upper case, or raise ValueError if invalid."""
        if not isinstance(unit, str) or unit.upper() not in cls.VALID_UNITS:
            raise ValueError(f"Invalid unit: {unit!r}. Use 'C', 'F' or 'K'.")
        return unit.upper()

    # ---------- Read-only attributes ----------
    @property
    def value(self) -> float:
        return self._value

    @property
    def unit(self) -> str:
        return self._unit

    # ---------- Conversions ----------
    def to_celsius(self) -> float:
        if self._unit == "C":
            return self._value
        if self._unit == "K":
            return self._value - 273.15
        return (self._value - 32) * 5 / 9  # from Fahrenheit

    def to_fahrenheit(self) -> float:
        if self._unit == "F":
            return self._value
        if self._unit == "C":
            return self._value * 9 / 5 + 32
        return (self._value - 273.15) * 9 / 5 + 32  # from Kelvin

    def to_kelvin(self) -> float:
        if self._unit == "K":
            return self._value
        if self._unit == "C":
            return self._value + 273.15
        return (self._value - 32) * 5 / 9 + 273.15  # from Fahrenheit

    def convert_to(self, target_unit: str) -> "Temperature":
        target = self._validate_unit(target_unit)
        converters = {
            "C": self.to_celsius,
            "F": self.to_fahrenheit,
            "K": self.to_kelvin,
        }
        return Temperature(converters[target](), target)

    # ---------- String representations ----------
    def __repr__(self) -> str:
        return f"Temperature({self._value!r}, {self._unit!r})"

    def __str__(self) -> str:
        return f"{self._value:.2f} °{self._unit}"

    # ---------- Comparisons (done in Kelvin, with tolerance) ----------
    def __eq__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return abs(self.to_kelvin() - other.to_kelvin()) < self.TOL

    def __ne__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() and not self == other

    def __le__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() or self == other

    def __gt__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() and not self == other

    def __ge__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() or self == other