from core.validators import (
    is_valid_decimal,
)


def validate_travel_row(row):

    errors = []

    distance = row.get(
        'distance_km'
    )

    if not is_valid_decimal(
        distance
    ):

        errors.append(
            'Invalid travel distance'
        )

    origin = row.get('origin')

    destination = row.get(
        'destination'
    )

    if not origin:

        errors.append(
            'Origin missing'
        )

    if not destination:

        errors.append(
            'Destination missing'
        )

    return {

        'valid': len(errors) == 0,

        'errors': errors,
    }