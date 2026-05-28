from core.models import Facility


def map_plant_to_facility(
    plant_code
):

    if not plant_code:

        return None

    facility = Facility.objects.filter(
        facility_code=plant_code
    ).first()

    return facility