from decimal import Decimal


# ─────────────────────────────────────
# DECIMAL VALIDATOR
# ─────────────────────────────────────

def is_valid_decimal(
    value
):

    try:

        Decimal(str(value))

        return True

    except Exception:

        return False


# ─────────────────────────────────────
# NON EMPTY STRING
# ─────────────────────────────────────

def is_non_empty_string(
    value
):

    if value is None:

        return False

    if not isinstance(value, str):

        return False

    return len(value.strip()) > 0


# ─────────────────────────────────────
# EMAIL VALIDATOR
# ─────────────────────────────────────

def is_valid_email(
    value
):

    if not value:

        return False

    return '@' in value


# ─────────────────────────────────────
# POSITIVE NUMBER
# ─────────────────────────────────────

def is_positive_number(
    value
):

    try:

        value = Decimal(str(value))

        return value >= 0

    except Exception:

        return False