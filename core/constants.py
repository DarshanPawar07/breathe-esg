# ─────────────────────────────────────
# INGESTION STATUS
# ─────────────────────────────────────

INGESTION_STATUS_CLEAN = 'clean'

INGESTION_STATUS_FLAGGED = 'flagged'

INGESTION_STATUS_FAILED = 'failed'


INGESTION_STATUS_CHOICES = [

    (
        INGESTION_STATUS_CLEAN,
        'Clean'
    ),

    (
        INGESTION_STATUS_FLAGGED,
        'Flagged'
    ),

    (
        INGESTION_STATUS_FAILED,
        'Failed'
    ),
]


# ─────────────────────────────────────
# EMISSION REVIEW STATUS
# ─────────────────────────────────────

STATUS_PENDING = 'pending'

STATUS_APPROVED = 'approved'

STATUS_FLAGGED = 'flagged'

STATUS_LOCKED = 'locked'


STATUS_CHOICES = [

    (
        STATUS_PENDING,
        'Pending'
    ),

    (
        STATUS_APPROVED,
        'Approved'
    ),

    (
        STATUS_FLAGGED,
        'Flagged'
    ),

    (
        STATUS_LOCKED,
        'Locked'
    ),
]


# ─────────────────────────────────────
# ESG SCOPES
# ─────────────────────────────────────

SCOPE_1 = 'Scope 1'

SCOPE_2 = 'Scope 2'

SCOPE_3 = 'Scope 3'


SCOPE_CHOICES = [

    (
        SCOPE_1,
        'Scope 1'
    ),

    (
        SCOPE_2,
        'Scope 2'
    ),

    (
        SCOPE_3,
        'Scope 3'
    ),
]


# ─────────────────────────────────────
# SOURCE TYPES
# ─────────────────────────────────────

SOURCE_SAP = 'SAP'

SOURCE_UTILITY = 'Utility'

SOURCE_TRAVEL = 'Travel'


SOURCE_TYPE_CHOICES = [

    (
        SOURCE_SAP,
        'SAP'
    ),

    (
        SOURCE_UTILITY,
        'Utility'
    ),

    (
        SOURCE_TRAVEL,
        'Travel'
    ),
]


# ─────────────────────────────────────
# FACILITY TYPES
# ─────────────────────────────────────

FACILITY_MANUFACTURING = (
    'manufacturing'
)

FACILITY_OFFICE = 'office'

FACILITY_WAREHOUSE = (
    'warehouse'
)


FACILITY_TYPE_CHOICES = [

    (
        FACILITY_MANUFACTURING,
        'Manufacturing'
    ),

    (
        FACILITY_OFFICE,
        'Office'
    ),

    (
        FACILITY_WAREHOUSE,
        'Warehouse'
    ),
]

# ─────────────────────────────────────
# UNIT MAPPINGS
# ─────────────────────────────────────

UNIT_MAPPINGS = {

    # Fuel

    'L': 'litres',

    'LTR': 'litres',

    'litre': 'litres',

    'litres': 'litres',

    'GAL': 'gallons',

    # Electricity

    'kWh': 'kWh',

    'MWh': 'MWh',

    # Distance

    'km': 'km',

    'mile': 'miles',
}

# ─────────────────────────────────────
# EMISSION FACTORS
# ─────────────────────────────────────

EMISSION_FACTORS = {

    # Diesel
    'diesel': {

        'factor': 2.65,

        'unit': 'litres',

        'scope': 'Scope 1',
    },

    # Petrol
    'petrol': {

        'factor': 2.31,

        'unit': 'litres',

        'scope': 'Scope 1',
    },

    # Electricity
    'electricity': {

        'factor': 0.82,

        'unit': 'kWh',

        'scope': 'Scope 2',
    },

    # Flight
    'flight': {

        'factor': 0.15,

        'unit': 'km',

        'scope': 'Scope 3',
    },

    # Hotel
    'hotel stay': {

        'factor': 15.0,

        'unit': 'night',

        'scope': 'Scope 3',
    },
}