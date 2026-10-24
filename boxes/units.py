from decimal import Decimal


_CENTIMETERS_PER_UNIT = {
    "mm": Decimal("0.1"),
    "cm": Decimal("1"),
    "m": Decimal("100"),
    "in": Decimal("2.54"),
}
_MILLIMETERS_PER_CENTIMETER = Decimal("10")
_INCHES_PER_CENTIMETER = Decimal("1") / Decimal("2.54")
_UNIT_FACTORS_FROM_CM = {
    "mm": _MILLIMETERS_PER_CENTIMETER,
    "cm": Decimal("1"),
    "m": Decimal("0.01"),
    "in": _INCHES_PER_CENTIMETER,
}


def _decimal_value(value):
    if isinstance(value, float):
        raise TypeError("Dimension values must use Decimal, not float.")
    try:
        return value if isinstance(value, Decimal) else Decimal(str(value))
    except (ValueError, TypeError, ArithmeticError) as error:
        raise ValueError(f"Invalid dimension value: {value!r}") from error


def _unit_factor(unit, factors):
    try:
        return factors[unit]
    except (KeyError, TypeError) as error:
        raise ValueError(
            f"Unknown dimension unit {unit!r}; supported units are mm, cm, m, and in."
        ) from error


def to_cm(value, unit):
    """Convert a dimension in mm, cm, m, or inches to canonical centimeters."""
    factor = _unit_factor(unit, _CENTIMETERS_PER_UNIT)
    return _decimal_value(value) * factor


def from_cm(value_cm, unit):
    """Convert a canonical centimeter dimension to mm, cm, m, or inches."""
    factor = _unit_factor(unit, _UNIT_FACTORS_FROM_CM)
    return _decimal_value(value_cm) * factor


def format_all_units(value_cm):
    """Return a Decimal conversion of a centimeter value in each supported unit."""
    return {
        unit: from_cm(value_cm, unit)
        for unit in ("mm", "cm", "m", "in")
    }
