import pandas as pd
from decimal import Decimal

from core.models import (
    TravelRecord,
    EmissionRecord,
)

from core.services.emissions.calculations import (
    calculate_travel_emissions
)


def ingest_travel_csv(
    file_path,
    tenant,
    upload_id
):

    dataframe = pd.read_csv(file_path)

    created_records = 0

    failed_records = 0

    for _, row in dataframe.iterrows():

        try:

            distance = Decimal(
                str(
                    row.get(
                        'distance_km',
                        0
                    )
                )
            )

            travel_record = (
                TravelRecord.objects.create(

                    tenant=tenant,

                    upload_id=upload_id,

                    raw_row=row.to_dict(),

                    ingestion_status='clean',

                    employee_id=row.get(
                        'employee_id',
                        ''
                    ),

                    travel_type=row.get(
                        'travel_type',
                        ''
                    ),

                    origin=row.get(
                        'origin',
                        ''
                    ),

                    destination=row.get(
                        'destination',
                        ''
                    ),

                    raw_distance_km=distance,

                    calculated_distance_km=(
                        distance
                    ),

                    distance_source='csv',
                )
            )

            emission_result = (
                calculate_travel_emissions(
                    distance
                )
            )

            EmissionRecord.objects.create(

                tenant=tenant,

                source_type='Travel',

                source_record_id=(
                    travel_record.id
                ),

                activity_type='Flight',

                original_quantity=distance,

                original_unit='km',

                normalized_quantity=distance,

                normalized_unit='km',

                scope='Scope 3',

                emission_factor=(
                    emission_result[
                        'emission_factor'
                    ]
                ),

                emission_factor_source=(
                    'DEFRA Aviation'
                ),

                co2e_kg=(
                    emission_result[
                        'co2e_kg'
                    ]
                ),

                status='pending',

                source_file_name=file_path,
            )

            created_records += 1

        except Exception:

            failed_records += 1

    return {

        'created': created_records,

        'failed': failed_records,
    }