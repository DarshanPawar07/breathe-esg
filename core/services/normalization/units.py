from decimal import Decimal


# ─────────────────────────────────────
# FUEL NORMALIZATION
# ─────────────────────────────────────

def normalize_fuel_unit(
    quantity,
    unit
):

    unit = str(unit).lower().strip()

    quantity = Decimal(str(quantity))

    # Already litres

    if unit in ['l', 'litre', 'litres']:

        return {

            'quantity': quantity,

            'unit': 'litres'
        }

    # Gallons → litres

    if unit in ['gal', 'gallon', 'gallons']:

        litres = quantity * Decimal('3.78541')

        return {

            'quantity': round(litres, 2),

            'unit': 'litres'
        }

    # Unknown

    return {

        'quantity': quantity,

        'unit': unit
    }


# ─────────────────────────────────────
# ELECTRICITY NORMALIZATION
# ─────────────────────────────────────

def normalize_electricity_unit(
    quantity,
    unit
):

    unit = str(unit).lower().strip()

    quantity = Decimal(str(quantity))

    # Already kWh

    if unit == 'kwh':

        return {

            'quantity': quantity,

            'unit': 'kWh'
        }

    # MWh → kWh

    if unit == 'mwh':

        converted = quantity * Decimal('1000')

        return {

            'quantity': converted,

            'unit': 'kWh'
        }

    return {

        'quantity': quantity,

        'unit': unit
    }


# ─────────────────────────────────────
# DISTANCE NORMALIZATION
# ─────────────────────────────────────

def normalize_distance_unit(
    quantity,
    unit
):

    unit = str(unit).lower().strip()

    quantity = Decimal(str(quantity))

    if unit in ['km', 'kilometer']:

        return {

            'quantity': quantity,

            'unit': 'km'
        }

    # Miles → KM

    if unit in ['mile', 'miles']:

        km = quantity * Decimal('1.60934')

        return {

            'quantity': round(km, 2),

            'unit': 'km'
        }

    return {

        'quantity': quantity,

        'unit': unit
    }