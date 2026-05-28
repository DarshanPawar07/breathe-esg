from decimal import Decimal


# ─────────────────────────────────────
# SAP RULES
# ─────────────────────────────────────

def is_suspicious_fuel_quantity(
    quantity
):

    quantity = Decimal(str(quantity))

    return quantity > Decimal('10000')


# ─────────────────────────────────────
# UTILITY RULES
# ─────────────────────────────────────

def is_suspicious_electricity_usage(
    consumption
):

    consumption = Decimal(
        str(consumption)
    )

    return consumption > Decimal(
        '100000'
    )


# ─────────────────────────────────────
# TRAVEL RULES
# ─────────────────────────────────────

def is_suspicious_travel_distance(
    distance
):

    distance = Decimal(str(distance))

    return distance > Decimal('20000')