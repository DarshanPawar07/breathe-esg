import pandas as pd

from decimal import Decimal

from uuid import uuid4

from core.models import (

    UtilityRecord,

    EmissionRecord,

    Facility,
)

from core.constants import (

    UNIT_MAPPINGS,

    EMISSION_FACTORS,
)

from core.services.ingestion.smart_mapper import (

    detect_column_mapping,
)


# ─────────────────────────────────────
# READ FILE
# ─────────────────────────────────────

def read_uploaded_file(file_path):

    if file_path.endswith('.xlsx'):

        return pd.read_excel(file_path)


    with open(

        file_path,

        'r',

        encoding='utf-8',

        errors='ignore'

    ) as f:

        sample = f.read(5000)


    separator = ','

    if '|' in sample:

        separator = '|'

    elif ';' in sample:

        separator = ';'

    elif '\t' in sample:

        separator = '\t'


    print(
        f'DETECTED SEPARATOR: {separator}'
    )


    return pd.read_csv(

        file_path,

        sep=separator,

        engine='python'
    )


# ─────────────────────────────────────
# PARSE DECIMAL
# ─────────────────────────────────────

def parse_decimal(value):

    if value is None:

        return Decimal('0')

    try:

        value = str(value).strip()

        if ',' in value and '.' in value:

            value = value.replace('.', '')
            value = value.replace(',', '.')

        elif ',' in value:

            value = value.replace(',', '.')

        return Decimal(value)

    except Exception:

        return Decimal('0')


# ─────────────────────────────────────
# NORMALIZE UNIT
# ─────────────────────────────────────

def normalize_unit(unit):

    if not unit:

        return None

    return UNIT_MAPPINGS.get(

        str(unit).upper(),

        str(unit).lower()
    )


# ─────────────────────────────────────
# INGEST UTILITY FILE
# ─────────────────────────────────────

def ingest_utility_csv(

    file_path,

    tenant,

    upload_id=None
):

    if not upload_id:

        upload_id = str(uuid4())


    df = read_uploaded_file(
        file_path
    )

    df = df.dropna(how='all')


    mapping = detect_column_mapping(
        df.columns
    )


    print('\nUTILITY MAPPING:')
    print(mapping)


    created_count = 0

    failed_count = 0

    flagged_count = 0


    for _, row in df.iterrows():

        try:

            mapped_data = {

                internal_field: row.get(
                    csv_column
                )

                for internal_field,
                csv_column

                in mapping.items()
            }


            facility_code = (
                mapped_data.get(
                    'facility'
                )
            )

            raw_quantity = (
                mapped_data.get(
                    'quantity'
                )
            )

            raw_unit = (
                mapped_data.get(
                    'unit'
                )
            )

            raw_date = (
                mapped_data.get(
                    'date'
                )
            )


            parsed_quantity = (
                parse_decimal(
                    raw_quantity
                )
            )

            parsed_unit = (
                normalize_unit(
                    raw_unit
                )
            )


            facility = (
                Facility.objects.filter(

                    tenant=tenant,

                    facility_code=
                        facility_code

                ).first()
            )


            ingestion_status = 'clean'


            if parsed_quantity <= 0:

                ingestion_status = 'failed'

                failed_count += 1


            utility_record = (
                UtilityRecord.objects.create(

                    tenant=tenant,

                    facility=facility,

                    upload_id=upload_id,

                    raw_row=row.to_dict(),

                    ingestion_status=
                        ingestion_status,

                    utility_type=
                        'Electricity',

                    raw_quantity=
                        str(raw_quantity),

                    parsed_quantity=
                        parsed_quantity,

                    raw_unit=
                        str(raw_unit),

                    parsed_unit=
                        parsed_unit,
                )
            )


            if ingestion_status != 'failed':

                emission_config = (
                    EMISSION_FACTORS.get(
                        'electricity'
                    )
                )

                emission_factor = Decimal(

                    str(
                        emission_config.get(
                            'factor',
                            0
                        )
                    )
                )

                co2e_kg = (

                    parsed_quantity *
                    emission_factor
                )


                EmissionRecord.objects.create(

                    tenant=tenant,

                    facility=facility,

                    source_type='Utility',

                    source_record_id=
                        utility_record.id,

                    activity_type=
                        'Electricity',

                    original_quantity=
                        parsed_quantity,

                    original_unit=
                        parsed_unit,

                    normalized_quantity=
                        parsed_quantity,

                    normalized_unit=
                        parsed_unit,

                    scope='Scope 2',

                    emission_factor=
                        emission_factor,

                    emission_factor_source=
                        'DEFRA 2023',

                    co2e_kg=co2e_kg,

                    status='pending',

                    source_file_name=
                        str(upload_id),
                )

            created_count += 1


        except Exception as e:

            print(
                'UTILITY ROW ERROR:',
                str(e)
            )

            failed_count += 1


    return {

        'created': created_count,

        'failed': failed_count,

        'flagged': flagged_count,
    }