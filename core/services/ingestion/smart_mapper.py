COLUMN_SYNONYMS = {

    # ─────────────────────────────
    # FACILITY
    # ─────────────────────────────

    'facility': [

        'facility',

        'facility_name',

        'plant',

        'plant_name',

        'site',

        'location',

        'factory',

        'werks',

        'werk',
    ],

    # ─────────────────────────────
    # QUANTITY
    # ─────────────────────────────

    'quantity': [

        'quantity',

        'qty',

        'consumption',

        'usage',

        'amount',

        'value',

        'fuel_used',

        'menge',

        'verbrauch',

        'verbrauchsmenge',
    ],

    # ─────────────────────────────
    # UNIT
    # ─────────────────────────────

    'unit': [

        'unit',

        'uom',

        'measurement',

        'units',

        'meins',

        'einheit',
    ],

    # ─────────────────────────────
    # ACTIVITY
    # ─────────────────────────────

    'activity': [

        'activity',

        'fuel',

        'material',

        'fuel_type',

        'type',

        'category',

        'materialbeschreibung',

        'material_description',

        'description',

        'maktx',
    ],

    # ─────────────────────────────
    # DATE
    # ─────────────────────────────

    'date': [

        'date',

        'posting_date',

        'invoice_date',

        'transaction_date',

        'bldat',

        'datum',
    ],

    # ─────────────────────────────
    # ORIGIN
    # ─────────────────────────────

    'origin': [

        'origin',

        'from',
    ],

    # ─────────────────────────────
    # DESTINATION
    # ─────────────────────────────

    'destination': [

        'destination',

        'to',
    ],
}


# ─────────────────────────────────────
# NORMALIZE COLUMN
# ─────────────────────────────────────

def normalize_column_name(name):

    return (

        str(name)
        .strip()
        .lower()
        .replace(' ', '_')
        .replace('-', '_')
        .replace('(', '')
        .replace(')', '')
        .replace('/', '_')
    )


# ─────────────────────────────────────
# DETECT MAPPING
# ─────────────────────────────────────

def detect_column_mapping(columns):

    detected = {}

    for original_column in columns:

        normalized = normalize_column_name(
            original_column
        )

        print(
            f'Checking column: '
            f'{normalized}'
        )

        for internal_field, synonyms in (
            COLUMN_SYNONYMS.items()
        ):

            for synonym in synonyms:

                synonym = normalize_column_name(
                    synonym
                )

                # Exact match

                if normalized == synonym:

                    detected[
                        internal_field
                    ] = original_column

                    break

                # Partial match

                if synonym in normalized:

                    detected[
                        internal_field
                    ] = original_column

                    break

    return detected