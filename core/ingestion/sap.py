import pandas as pd
from decimal import Decimal

from core.models import (
    SAPRecord,
    EmissionRecord,
    Facility,
)

from core.services.emissions.calculations import (
    calculate_fuel_emissions
)


def ingest_sap_csv(
    file_path,
    tenant,
    upload_id
):

    dataframe = pd.read_csv(file_path)

    created_records = 0

    flagged_records = 0

    failed_records = 0

    for _, row in dataframe.iterrows():

        try:

            quantity = Decimal(
                str(row.get('MENGE', 0))
                .replace(',', '')
            )

            plant_code = row.get(
                'WERKS'
            )

            facility = Facility.objects.filter(
                facility_code=plant_code
            ).first()

            sap_record = SAPRecord.objects.create(

                tenant=tenant,

                facility=facility,

                upload_id=upload_id,

                raw_row=row.to_dict(),

                ingestion_status='clean',

                material_code=row.get(
                    'MATNR',
                    ''
                ),

                material_name=row.get(
                    'MAKTX',
                    ''
                ),

                plant_code=plant_code,

                raw_quantity=str(
                    row.get('MENGE')
                ),

                parsed_quantity=quantity,

                raw_unit=row.get(
                    'MEINS',
                    ''
                ),

                parsed_unit='litres',

                description=row.get(
                    'SGTXT',
                    ''
                ),
            )

            emission_result = (
                calculate_fuel_emissions(
                    quantity
                )
            )

            EmissionRecord.objects.create(

                tenant=tenant,

                facility=facility,

                source_type='SAP',

                source_record_id=sap_record.id,

                activity_type='Diesel',

                original_quantity=quantity,

                original_unit='L',

                normalized_quantity=quantity,

                normalized_unit='litres',

                scope='Scope 1',

                emission_factor=(
                    emission_result[
                        'emission_factor'
                    ]
                ),

                emission_factor_source='DEFRA',

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

        'flagged': flagged_records,

        'failed': failed_records,
    }