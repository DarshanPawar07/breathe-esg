from core.validators import (
    is_valid_decimal,
    is_non_empty_string,
)

from core.services.validation.suspicious_rules import (
    is_suspicious_fuel_quantity
)


def validate_sap_row(row):

    errors = []

    warnings = []

    quantity = row.get('MENGE')

    material_name = row.get('MAKTX')

    if not is_non_empty_string(
        material_name
    ):

        errors.append(
            'Material name missing'
        )

    if not is_valid_decimal(
        quantity
    ):

        errors.append(
            'Invalid quantity'
        )

    if (
        is_valid_decimal(quantity)
        and
        is_suspicious_fuel_quantity(
            quantity
        )
    ):

        warnings.append(
            'Suspiciously high fuel quantity'
        )

    return {

        'valid': len(errors) == 0,

        'errors': errors,

        'warnings': warnings,
    }