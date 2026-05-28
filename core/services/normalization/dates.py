from datetime import datetime


SUPPORTED_DATE_FORMATS = [

    '%d.%m.%y',

    '%Y-%m-%d',

    '%d/%m/%Y',

    '%m/%d/%Y',
]


def normalize_date(date_value):

    if not date_value:

        return None

    date_value = str(date_value).strip()

    for date_format in SUPPORTED_DATE_FORMATS:

        try:

            return datetime.strptime(
                date_value,
                date_format
            ).date()

        except Exception:

            continue

    return None