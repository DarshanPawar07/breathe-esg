from core.validators import (
    is_valid_decimal,
)


def validate_utility_row(row):

    errors = []

    consumption = row.get(
        'consumption'
    )

    if not is_valid_decimal(
        consumption
    ):

        errors.append(
            'Invalid consumption value'
        )

    provider_name = row.get(
        'provider_name'
    )

    if not provider_name:

        errors.append(
            'Provider name missing'
        )

    return {

        'valid': len(errors) == 0,

        'errors': errors,
    }