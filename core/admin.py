from django.contrib import admin

from .models import (

    Tenant,

    Facility,

    SAPRecord,

    UtilityRecord,

    TravelRecord,

    EmissionRecord,
)


# ─────────────────────────────────────
# TENANT
# ─────────────────────────────────────

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'name',

        'created_at',
    )

    search_fields = (

        'name',
    )


# ─────────────────────────────────────
# FACILITY
# ─────────────────────────────────────

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):

    list_display = (

        'facility_code',

        'facility_name',

        'facility_type',

        'city',

        'country',

        'is_active',
    )

    search_fields = (

        'facility_code',

        'facility_name',
    )

    list_filter = (

        'facility_type',

        'is_active',
    )


# ─────────────────────────────────────
# SAP RECORD
# ─────────────────────────────────────

@admin.register(SAPRecord)
class SAPRecordAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'material_name',

        'plant_code',

        'parsed_quantity',

        'parsed_unit',

        'ingestion_status',

        'created_at',
    )

    search_fields = (

        'material_name',

        'plant_code',
    )

    list_filter = (

        'ingestion_status',
    )


# ─────────────────────────────────────
# UTILITY RECORD
# ─────────────────────────────────────

@admin.register(UtilityRecord)
class UtilityRecordAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'utility_type',

        'parsed_quantity',

        'parsed_unit',

        'ingestion_status',

        'created_at',
    )

    search_fields = (

        'utility_type',
    )

    list_filter = (

        'ingestion_status',
    )


# ─────────────────────────────────────
# TRAVEL RECORD
# ─────────────────────────────────────
@admin.register(TravelRecord)
class TravelRecordAdmin(admin.ModelAdmin):

    list_display = [

        'id',

        'tenant',

        'employee_id',

        'travel_type',

        'origin',

        'destination',

        'raw_distance_km',

        'ingestion_status',

        'created_at',
    ]

    search_fields = [

        'employee_id',

        'origin',

        'destination',
    ]

    list_filter = [

        'travel_type',

        'ingestion_status',
    ]

# ─────────────────────────────────────
# EMISSION RECORD
# ─────────────────────────────────────

@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'activity_type',

        'source_type',

        'scope',

        'co2e_kg',

        'status',

        'created_at',
    )

    search_fields = (

        'activity_type',

        'source_type',
    )

    list_filter = (

        'scope',

        'status',

        'source_type',
    )