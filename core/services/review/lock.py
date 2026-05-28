from django.utils import timezone

from core.models import EmissionRecord


def lock_emission_record(
    record_id
):

    record = EmissionRecord.objects.get(
        id=record_id
    )

    record.status = 'locked'

    record.locked_at = timezone.now()

    record.save()

    return record