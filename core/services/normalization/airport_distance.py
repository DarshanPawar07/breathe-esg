AIRPORT_DISTANCE_MAP = {

    ('BOM', 'DEL'): 1150,

    ('DEL', 'BLR'): 1740,

    ('BLR', 'HYD'): 500,

    ('BOM', 'BLR'): 840,

    ('DEL', 'HYD'): 1250,
}


def get_airport_distance(
    origin,
    destination
):

    origin = str(origin).upper().strip()

    destination = (
        str(destination)
        .upper()
        .strip()
    )

    if (origin, destination) in (
        AIRPORT_DISTANCE_MAP
    ):

        return AIRPORT_DISTANCE_MAP[
            (origin, destination)
        ]

    if (destination, origin) in (
        AIRPORT_DISTANCE_MAP
    ):

        return AIRPORT_DISTANCE_MAP[
            (destination, origin)
        ]

    return None