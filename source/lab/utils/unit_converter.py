################################################
# Functions to convert units
# Marta Huertas
# Grup d'Epidemiologia Cardiovascular - IMIM
# Data: 10/12/2024
################################################

# Functions used to convert from one unit to another

from .factors import factor_dict, base_units
import numpy as np
import pandas as pd

def _parse_unit(unit):
    """Parses a single unit to extract the base unit and prefix factor."""
    if not isinstance(unit, str):
        # Return None if the unit is not a string
        return None, None
    
    if unit in base_units:
        base_unit = unit
        prefix_factor = 1
    elif len(unit) >= 1 and unit[0] in factor_dict:
        prefix = unit[0]
        base_unit = unit[1:]
        prefix_factor = factor_dict[prefix]
    else:
        # Return None to indicate an unrecognized unit
        return None, None
    
    return base_unit, prefix_factor

def unit_to_base(unit):
    """Converts a unit (potentially with a prefix and/or a fraction) into its base unit form and factor."""
    if "/" in unit:
        numerator, denominator = unit.split("/")
        base_numerator, factor_numerator = _parse_unit(numerator)
        base_denominator, factor_denominator = _parse_unit(denominator)

        if base_numerator is None or base_denominator is None:
            return None  # Invalid unit

        prefix_factor = factor_numerator / factor_denominator
        return base_numerator, base_denominator, prefix_factor
    else:
        base_unit, prefix_factor = _parse_unit(unit)
        if base_unit is None:
            return None  # Invalid unit
        return base_unit, prefix_factor

def convert(value, from_unit, to_unit):
    """Convert a value from one unit to another."""
    from_parts = unit_to_base(from_unit)
    to_parts = unit_to_base(to_unit)

    if len(from_parts) != len(to_parts):
        raise ValueError(
            f"Incompatible units for conversion: {from_unit} ({from_parts}) and {to_unit} ({to_parts})"
        )

    if len(from_parts) not in {2, 3}:
        raise ValueError(
            f"Unsupported unit format: {from_unit} ({from_parts}) or {to_unit} ({to_parts})"
        )

    # Unpack unit components
    try:
        from_bases, from_factor = from_parts[:-1], from_parts[-1]
        to_bases, to_factor = to_parts[:-1], to_parts[-1]
    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid unit structure: {from_unit} ({from_parts}) or {to_unit} ({to_parts})"
        )

    # Check base compatibility
    if from_bases != to_bases:
        raise ValueError(
            f"Cannot convert between incompatible base units: "
            f"{from_unit} ({from_bases}) and {to_unit} ({to_bases})"
        )

    # Perform the conversion
    return value * from_factor / to_factor

def processing(df):
    """Processes a DataFrame to convert values from one unit to another. """
    def convert_row(row):
        try:
            # Check if lab_resultat is numeric
            if isinstance(row["lab_resultat"], (int, float)):
                from_base = unit_to_base(row["unitat_mesura"])
                to_base = unit_to_base(row["common_units"])

                # Skip conversion if units are invalid
                if from_base is None or to_base is None:
                    return None

                # Perform conversion
                return convert(row["lab_resultat"], row["unitat_mesura"], row["common_units"])
            else:
                return None  # Skip non-numeric values
        except (ValueError, TypeError) as e:
            print(f"Conversion error for row {row.name}: {e}")
            return None

    # Apply conversion to each row
    df["transformed_value"] = df.apply(convert_row, axis=1)
    return df