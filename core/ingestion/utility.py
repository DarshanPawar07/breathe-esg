import pandas as pd
from decimal import Decimal

from core.models import (
    UtilityRecord,
    EmissionRecord,
    Facility,
)

from core.services.emissions.calculations import (
    calculate_electricity_emissions
)


def ingest_utility_csv(
    file_path,
    tenant,
    upload_id
):

    dataframe = pd.read_csv(file_path)

    created_records = 0

    failed_records = 0

    for _, row in dataframe.iterrows():

        try:

            consumption = Decimal(
                str(row.get(
                    'consumption',
                    0
                ))
            )

            facility_code = row.get(
                'facility_code'
            )

            facility = Facility.objects.filter(
                facility_code=facility_code
            ).first()

            utility_record = (
                UtilityRecord.objects.create(

                    tenant=tenant,

                    facility=facility,

                    upload_id=upload_id,

                    raw_row=row.to_dict(),

                    ingestion_status='clean',

                    account_number=row.get(
                        'account_number',
                        ''
                    ),

                    meter_id=row.get(
                        'meter_id',
                        ''
                    ),

                    raw_consumption=str(
                        consumption
                    ),

                    raw_unit=row.get(
                        'unit',
                        ''
                    ),

                    normalized_consumption=(
                        consumption
                    ),

                    normalized_unit='kWh',

                    provider_name=row.get(
                        'provider_name',
                        ''
                    ),
                )
            )

            emission_result = (
                calculate_electricity_emissions(
                    consumption
                )
            )

            EmissionRecord.objects.create(

                tenant=tenant,

                facility=facility,

                source_type='Utility',

                source_record_id=(
                    utility_record.id
                ),

                activity_type='Electricity',

                original_quantity=consumption,

                original_unit='kWh',

                normalized_quantity=(
                    consumption
                ),

                normalized_unit='kWh',

                scope='Scope 2',

                emission_factor=(
                    emission_result[
                        'emission_factor'
                    ]
                ),

                emission_factor_source=(
                    'India Grid'
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