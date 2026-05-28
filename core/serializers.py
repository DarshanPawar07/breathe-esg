from rest_framework import serializers

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

class TenantSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Tenant

        fields = '__all__'


# ─────────────────────────────────────
# FACILITY
# ─────────────────────────────────────

class FacilitySerializer(
    serializers.ModelSerializer
):

    tenant_name = serializers.CharField(
        source='tenant.name',
        read_only=True
    )

    class Meta:

        model = Facility

        fields = '__all__'


# ─────────────────────────────────────
# SAP
# ─────────────────────────────────────

class SAPRecordSerializer(
    serializers.ModelSerializer
):

    facility_name = (
        serializers.SerializerMethodField()
    )

    class Meta:

        model = SAPRecord

        fields = '__all__'

    def get_facility_name(
        self,
        obj
    ):

        if obj.facility:

            return (
                f'{obj.facility.facility_code} '
                f'{obj.facility.facility_name}'
            )

        return None


# ─────────────────────────────────────
# UTILITY
# ─────────────────────────────────────

class UtilityRecordSerializer(
    serializers.ModelSerializer
):

    facility_name = (
        serializers.SerializerMethodField()
    )

    class Meta:

        model = UtilityRecord

        fields = '__all__'

    def get_facility_name(
        self,
        obj
    ):

        if obj.facility:

            return (
                f'{obj.facility.facility_code} '
                f'{obj.facility.facility_name}'
            )

        return None


# ─────────────────────────────────────
# TRAVEL
# ─────────────────────────────────────

class TravelRecordSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = TravelRecord

        fields = '__all__'


# ─────────────────────────────────────
# EMISSION RECORDS
# ─────────────────────────────────────

class EmissionRecordSerializer(
    serializers.ModelSerializer
):

    tenant_name = serializers.CharField(
        source='tenant.name',
        read_only=True
    )

    facility_name = (
        serializers.SerializerMethodField()
    )

    facility_code = (
        serializers.SerializerMethodField()
    )

    formatted_co2e = (
        serializers.SerializerMethodField()
    )

    class Meta:

        model = EmissionRecord

        fields = '__all__'


    # ─────────────────────────────
    # FACILITY NAME
    # ─────────────────────────────

    def get_facility_name(
        self,
        obj
    ):

        if obj.facility:

            return (
                obj.facility.facility_name
            )

        return None


    # ─────────────────────────────
    # FACILITY CODE
    # ─────────────────────────────

    def get_facility_code(
        self,
        obj
    ):

        if obj.facility:

            return (
                obj.facility.facility_code
            )

        return None


    # ─────────────────────────────
    # FORMATTED CO₂
    # ─────────────────────────────

    def get_formatted_co2e(
        self,
        obj
    ):

        return (
            f'{obj.co2e_kg:,.2f} kg'
        )