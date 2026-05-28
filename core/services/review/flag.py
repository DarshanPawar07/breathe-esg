from django.utils import timezone

from core.models import EmissionRecord


def flag_emission_record(
    record_id,
    reviewer_email,
    reason
):

    record = EmissionRecord.objects.get(
        id=record_id
    )

    # Locked records cannot change

    if record.status == 'locked':

        return record

    record.status = 'flagged'

    record.reviewer_email = reviewer_email

    record.review_notes = reason

    record.reviewed_at = timezone.now()

    record.save()

    return record