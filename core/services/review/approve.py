from django.utils import timezone

from core.models import EmissionRecord


def approve_emission_record(
    record_id,
    reviewer_email
):

    record = EmissionRecord.objects.get(
        id=record_id
    )

    # Do not modify locked records

    if record.status == 'locked':

        return record

    record.status = 'approved'

    record.reviewer_email = reviewer_email

    record.reviewed_at = timezone.now()

    record.review_notes = (
        'Approved by analyst'
    )

    record.save()

    return record