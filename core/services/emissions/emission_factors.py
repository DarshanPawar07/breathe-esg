from decimal import Decimal


# ─────────────────────────────────────
# EMISSION FACTORS
# Values are simplified demo values
# kg CO₂e per unit
# ─────────────────────────────────────

EMISSION_FACTORS = {

    # Fuel
    'diesel_litre': Decimal('2.68'),

    # Electricity
    'electricity_kwh': Decimal('0.82'),

    # Flight travel
    'flight_km': Decimal('0.15'),

    # Hotel stays
    'hotel_night': Decimal('15.00'),
}


# ─────────────────────────────────────
# GETTERS
# ─────────────────────────────────────

def get_diesel_factor():

    return EMISSION_FACTORS[
        'diesel_litre'
    ]


def get_electricity_factor():

    return EMISSION_FACTORS[
        'electricity_kwh'
    ]


def get_flight_factor():

    return EMISSION_FACTORS[
        'flight_km'
    ]


def get_hotel_factor():

    return EMISSION_FACTORS[
        'hotel_night'
    ]