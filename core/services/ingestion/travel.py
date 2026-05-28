import pandas as pd

from decimal import Decimal

from core.models import (

    TravelRecord,

    EmissionRecord,

    Facility,
)

from core.constants import (

    EMISSION_FACTORS,
)


# ─────────────────────────────────────
# INGEST TRAVEL CSV
# ─────────────────────────────────────

def ingest_travel_csv(

    file_path,

    tenant,

    upload_id,
):

    # ─────────────────────────────
    # READ CSV SAFELY
    # ─────────────────────────────

    df = pd.read_csv(

        file_path,

        encoding='utf-8',

        on_bad_lines='skip'
    )

    created = 0

    failed = 0


    # ─────────────────────────────
    # ITERATE ROWS
    # ─────────────────────────────

    for _, row in df.iterrows():

        try:

            # ─────────────────────────
            # EXTRACT VALUES
            # ─────────────────────────

            employee_id = str(

                row.get(
                    'employee_id',
                    ''
                )
            ).strip()


            travel_type = str(

                row.get(
                    'travel_type',
                    'flight'
                )
            ).strip().lower()


            origin = str(

                row.get(
                    'origin',
                    ''
                )
            ).strip()


            destination = str(

                row.get(
                    'destination',
                    ''
                )
            ).strip()


            facility_code = str(

                row.get(
                    'facility_code',
                    ''
                )
            ).strip()


            # ─────────────────────────
            # DISTANCE
            # ─────────────────────────

            distance_raw = row.get(
                'distance_km',
                0
            )

            try:

                distance_km = Decimal(
                    str(distance_raw)
                )

            except Exception:

                distance_km = Decimal('0')


            # ─────────────────────────
            # FIND FACILITY
            # ─────────────────────────

            facility = (

                Facility.objects.filter(

                    facility_code=
                    facility_code

                ).first()
            )


            # ─────────────────────────
            # CREATE TRAVEL RECORD
            # ─────────────────────────

            travel_record = (

                TravelRecord.objects.create(

                    tenant=tenant,

                    facility=facility,

                    upload_id=upload_id,

                   raw_row={

    key: str(value)

    for key, value in row.to_dict().items()
},

                    employee_id=
                        employee_id,

                    travel_type=
                        travel_type,

                    origin=origin,

                    destination=
                        destination,

                    raw_distance_km=
                        distance_km,

                    calculated_distance_km=
                        distance_km,

                    distance_source=
                        'csv',
                )
            )


            # ─────────────────────────
            # EMISSION FACTOR
            # ─────────────────────────

            factor_key = 'flight'

            if 'hotel' in travel_type:

                factor_key = 'hotel stay'


            factor_data = (
                EMISSION_FACTORS.get(
                    factor_key
                )
            )


            emission_factor = Decimal(

                str(
                    factor_data[
                        'factor'
                    ]
                )
            )


            scope = factor_data[
                'scope'
            ]


            # ─────────────────────────
            # CO₂ CALCULATION
            # ─────────────────────────

            co2e_kg = (

                distance_km *

                emission_factor
            )


            # ─────────────────────────
            # CREATE EMISSION RECORD
            # ─────────────────────────

            EmissionRecord.objects.create(

                tenant=tenant,

                facility=facility,

                source_type='Travel',

                source_record_id=
                    travel_record.id,

                activity_type=
                    travel_type,

                original_quantity=
                    distance_km,

                original_unit='km',

                normalized_quantity=
                    distance_km,

                normalized_unit='km',

                scope=scope,

                emission_factor=
                    emission_factor,

                emission_factor_source=
                    'Default Travel Factor',

                co2e_kg=co2e_kg,

                source_file_name=
                    upload_id,
            )

            created += 1


        except Exception as error:

            print(
                'Travel row failed:',
                error
            )

            failed += 1


    # ─────────────────────────────
    # RESULT
    # ─────────────────────────────

    return {

        'created': created,

        'failed': failed,
    }