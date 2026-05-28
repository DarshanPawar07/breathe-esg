# ─────────────────────────────────────
# ESG SCOPE MAPPING
# ─────────────────────────────────────

ACTIVITY_SCOPE_MAP = {

    # Scope 1
    'diesel': 'Scope 1',

    'petrol': 'Scope 1',

    'natural gas': 'Scope 1',

    # Scope 2
    'electricity': 'Scope 2',

    # Scope 3
    'flight': 'Scope 3',

    'hotel': 'Scope 3',

    'ground travel': 'Scope 3',
}


def get_scope_for_activity(
    activity
):

    if not activity:

        return 'Scope 3'

    activity = (
        str(activity)
        .lower()
        .strip()
    )

    return ACTIVITY_SCOPE_MAP.get(
        activity,
        'Scope 3'
    )