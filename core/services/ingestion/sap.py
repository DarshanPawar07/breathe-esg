import pandas as pd

from decimal import Decimal

from uuid import uuid4

from core.models import (

    SAPRecord,

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
# READ FILE SMARTLY
# ─────────────────────────────────────

def read_uploaded_file(file_path):

    # XLSX support

    if file_path.endswith('.xlsx'):

        print('Detected Excel file')

        return pd.read_excel(file_path)


    # Read sample for separator detection

    with open(

        file_path,

        'r',

        encoding='utf-8',

        errors='ignore'

    ) as f:

        sample = f.read(5000)


    # Default separator

    separator = ','


    # Detect separator dynamically

    if '|' in sample:

        separator = '|'

    elif ';' in sample:

        separator = ';'

    elif '\t' in sample:

        separator = '\t'


    print(
        f'DETECTED SEPARATOR: {separator}'
    )


    # Read CSV

    df = pd.read_csv(

        file_path,

        sep=separator,

        engine='python'
    )


    print('\nDATAFRAME PREVIEW:')
    print(df.head())


    return df

# ─────────────────────────────────────
# NORMALIZE UNIT
# ─────────────────────────────────────

def normalize_unit(unit):

    if not unit:

        return None

    unit = str(unit).strip()

    return UNIT_MAPPINGS.get(

        unit.upper(),

        unit.lower()
    )


# ─────────────────────────────────────
# PARSE DECIMAL
# ─────────────────────────────────────

def parse_decimal(value):

    if value is None:

        return Decimal('0')

    try:

        value = str(value).strip()

        # German format:
        # 1.500,25

        if ',' in value and '.' in value:

            value = value.replace('.', '')
            value = value.replace(',', '.')

        # European decimal:
        # 1500,25

        elif ',' in value:

            value = value.replace(',', '.')

        return Decimal(value)

    except Exception as e:

        print(
            'DECIMAL PARSE ERROR:',
            value,
            str(e)
        )

        return Decimal('0')


# ─────────────────────────────────────
# DETECT SUSPICIOUS
# ─────────────────────────────────────

def detect_suspicious(quantity):

    if quantity > 100000:

        return True

    return False


# ─────────────────────────────────────
# DETECT ACTIVITY TYPE
# ─────────────────────────────────────

def detect_activity_type(text):

    if not text:

        return 'General Activity'

    text = str(text).lower()

    if 'diesel' in text:

        return 'Diesel'

    if 'petrol' in text:

        return 'Petrol'

    if 'electricity' in text:

        return 'Electricity'

    if 'hotel' in text:

        return 'Hotel Stay'

    if 'flight' in text:

        return 'Flight'

    return 'General Activity'


# ─────────────────────────────────────
# GET EMISSION CONFIG
# ─────────────────────────────────────

def get_emission_config(activity):

    activity = str(activity).lower()

    if 'diesel' in activity:

        return EMISSION_FACTORS.get(
            'diesel'
        )

    if 'petrol' in activity:

        return EMISSION_FACTORS.get(
            'petrol'
        )

    if 'electricity' in activity:

        return EMISSION_FACTORS.get(
            'electricity'
        )

    if 'flight' in activity:

        return EMISSION_FACTORS.get(
            'flight'
        )

    if 'hotel' in activity:

        return EMISSION_FACTORS.get(
            'hotel stay'
        )

    return {

        'factor': 0,

        'scope': 'Scope 3',
    }


# ─────────────────────────────────────
# INGEST FILE
# ─────────────────────────────────────

def ingest_sap_csv(

    file_path,

    tenant,

    upload_id=None
):

    if not upload_id:

        upload_id = str(uuid4())


    # Read uploaded file

    df = read_uploaded_file(
        file_path
    )


    # Remove fully empty rows

    df = df.dropna(how='all')


    # Detect columns dynamically

    mapping = detect_column_mapping(
        df.columns
    )


    print('\n======================')
    print('CSV COLUMNS:')
    print(list(df.columns))

    print('\nDETECTED MAPPING:')
    print(mapping)
    print('======================\n')


    created_count = 0

    failed_count = 0

    flagged_count = 0


    # Critical validation

    if 'quantity' not in mapping:

        print(
            'Quantity column not detected'
        )

        return {

            'created': 0,

            'failed': 0,

            'flagged': 0,
        }


    # ─────────────────────────────────
    # PROCESS ROWS
    # ─────────────────────────────────

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


            # ─────────────────────────
            # EXTRACT VALUES
            # ─────────────────────────

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

            activity_text = (
                mapped_data.get(
                    'activity'
                )
            )

            raw_date = (
                mapped_data.get(
                    'date'
                )
            )


            # ─────────────────────────
            # NORMALIZE
            # ─────────────────────────

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

            activity_type = (
                detect_activity_type(
                    activity_text
                )
            )


            print(
                'RAW QUANTITY:',
                raw_quantity
            )

            print(
                'PARSED QUANTITY:',
                parsed_quantity
            )


            # ─────────────────────────
            # FACILITY LOOKUP
            # ─────────────────────────

            facility = (
                Facility.objects.filter(

                    tenant=tenant,

                    facility_code=
                        facility_code

                ).first()
            )


            # ─────────────────────────
            # STATUS
            # ─────────────────────────

            ingestion_status = 'clean'


            if parsed_quantity <= 0:

                ingestion_status = 'failed'

                failed_count += 1


            elif detect_suspicious(
                parsed_quantity
            ):

                ingestion_status = 'flagged'

                flagged_count += 1


            # ─────────────────────────
            # CREATE SAP RECORD
            # ─────────────────────────

            sap_record = SAPRecord.objects.create(

                tenant=tenant,

                facility=facility,

                upload_id=upload_id,

                raw_row=row.to_dict(),

                ingestion_status=
                    ingestion_status,

                material_code=
                    str(activity_type),

                material_name=
                    str(activity_text),

                plant_code=
                    str(facility_code),

                raw_quantity=
                    str(raw_quantity),

                parsed_quantity=
                    parsed_quantity,

                raw_unit=
                    str(raw_unit),

                parsed_unit=
                    parsed_unit,

                description=
                    str(activity_text),
            )


            # ─────────────────────────
            # CREATE EMISSION RECORD
            # ─────────────────────────

            if ingestion_status != 'failed':

                emission_config = (
                    get_emission_config(
                        activity_type
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

                scope = (
                    emission_config.get(
                        'scope',
                        'Scope 3'
                    )
                )

                co2e_kg = (

                    parsed_quantity *
                    emission_factor
                )


                EmissionRecord.objects.create(

                    tenant=tenant,

                    facility=facility,

                    source_type='SAP',

                    source_record_id=
                        sap_record.id,

                    activity_type=
                        activity_type,

                    original_quantity=
                        parsed_quantity,

                    original_unit=
                        parsed_unit,

                    normalized_quantity=
                        parsed_quantity,

                    normalized_unit=
                        parsed_unit,

                    scope=scope,

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
                'ROW PROCESSING ERROR:',
                str(e)
            )

            failed_count += 1


    # ─────────────────────────────────
    # FINAL SUMMARY
    # ─────────────────────────────────

    return {

        'created': created_count,

        'failed': failed_count,

        'flagged': flagged_count,
    }