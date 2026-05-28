from decimal import Decimal

from core.services.emissions.emission_factors import (

    get_diesel_factor,

    get_electricity_factor,

    get_flight_factor,

    get_hotel_factor,
)


# ─────────────────────────────────────
# FUEL EMISSIONS
# ─────────────────────────────────────

def calculate_fuel_emissions(
    quantity
):

    quantity = Decimal(str(quantity))

    factor = get_diesel_factor()

    co2e = quantity * factor

    return {

        'emission_factor': factor,

        'co2e_kg': round(co2e, 2),
    }


# ─────────────────────────────────────
# ELECTRICITY EMISSIONS
# ─────────────────────────────────────

def calculate_electricity_emissions(
    consumption
):

    consumption = Decimal(
        str(consumption)
    )

    factor = get_electricity_factor()

    co2e = consumption * factor

    return {

        'emission_factor': factor,

        'co2e_kg': round(co2e, 2),
    }


# ─────────────────────────────────────
# TRAVEL EMISSIONS
# ─────────────────────────────────────

def calculate_travel_emissions(
    distance
):

    distance = Decimal(str(distance))

    factor = get_flight_factor()

    co2e = distance * factor

    return {

        'emission_factor': factor,

        'co2e_kg': round(co2e, 2),
    }


# ─────────────────────────────────────
# HOTEL EMISSIONS
# ─────────────────────────────────────

def calculate_hotel_emissions(
    nights
):

    nights = Decimal(str(nights))

    factor = get_hotel_factor()

    co2e = nights * factor

    return {

        'emission_factor': factor,

        'co2e_kg': round(co2e, 2),
    }