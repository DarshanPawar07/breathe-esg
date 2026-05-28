from django.db import models


# ─────────────────────────────────────
# TENANT
# ─────────────────────────────────────

class Tenant(models.Model):

    name = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# ─────────────────────────────────────
# FACILITY
# ─────────────────────────────────────

class Facility(models.Model):

    FACILITY_TYPES = [

        ('manufacturing', 'Manufacturing'),

        ('office', 'Office'),

        ('warehouse', 'Warehouse'),
    ]

    tenant = models.ForeignKey(

        Tenant,

        on_delete=models.CASCADE,

        related_name='facilities'
    )

    facility_code = models.CharField(
        max_length=50
    )

    facility_name = models.CharField(
        max_length=255
    )

    facility_type = models.CharField(

        max_length=50,

        choices=FACILITY_TYPES,

        default='manufacturing'
    )

    city = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    country = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f'{self.facility_code} - '
            f'{self.facility_name}'
        )


# ─────────────────────────────────────
# BASE INGESTION MODEL
# ─────────────────────────────────────

class BaseIngestionModel(
    models.Model
):

    INGESTION_STATUS = [

        ('clean', 'Clean'),

        ('flagged', 'Flagged'),

        ('failed', 'Failed'),
    ]

    tenant = models.ForeignKey(

        Tenant,

        on_delete=models.CASCADE
    )

    facility = models.ForeignKey(

        Facility,

        on_delete=models.SET_NULL,

        null=True,

        blank=True
    )

    upload_id = models.CharField(

        max_length=255,

        blank=True,

        null=True
    )

    raw_row = models.JSONField(
        default=dict
    )

    ingestion_status = models.CharField(

        max_length=20,

        choices=INGESTION_STATUS,

        default='clean'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        abstract = True


# ─────────────────────────────────────
# SAP RECORD
# ─────────────────────────────────────

class SAPRecord(
    BaseIngestionModel
):

    material_code = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    material_name = models.CharField(

        max_length=255,

        blank=True,

        null=True
    )

    plant_code = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    raw_quantity = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    parsed_quantity = models.DecimalField(

        max_digits=15,

        decimal_places=2,

        default=0
    )

    raw_unit = models.CharField(

        max_length=50,

        blank=True,

        null=True
    )

    parsed_unit = models.CharField(

        max_length=50,

        blank=True,

        null=True
    )

    description = models.TextField(

        blank=True,

        null=True
    )

    def __str__(self):

        return (
            f'SAP - '
            f'{self.material_name}'
        )


# ─────────────────────────────────────
# UTILITY RECORD
# ─────────────────────────────────────

class UtilityRecord(
    BaseIngestionModel
):

    utility_type = models.CharField(

        max_length=255,

        blank=True,

        null=True
    )

    raw_quantity = models.CharField(

        max_length=255,

        blank=True,

        null=True
    )

    parsed_quantity = models.DecimalField(

        max_digits=15,

        decimal_places=2,

        null=True,

        blank=True
    )

    raw_unit = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    parsed_unit = models.CharField(

        max_length=100,

        blank=True,

        null=True
    )

    provider = models.CharField(

        max_length=255,

        blank=True,

        null=True
    )

    def __str__(self):

        return (
            f'UtilityRecord {self.id}'
        )


# ─────────────────────────────────────
# TRAVEL RECORD
# ─────────────────────────────────────
class TravelRecord(
    BaseIngestionModel
):

    employee_id = models.CharField(
        max_length=100
    )

    travel_type = models.CharField(
        max_length=100
    )

    origin = models.CharField(
        max_length=100
    )

    destination = models.CharField(
        max_length=100
    )

    raw_distance_km = (
        models.DecimalField(

            max_digits=15,

            decimal_places=2
        )
    )

    calculated_distance_km = (
        models.DecimalField(

            max_digits=15,

            decimal_places=2
        )
    )

    distance_source = models.CharField(
        max_length=100
    )

    def __str__(self):

        return (
            f'{self.employee_id} - '
            f'{self.travel_type}'
        )

# ─────────────────────────────────────
# EMISSION RECORD
# ─────────────────────────────────────

class EmissionRecord(models.Model):

    STATUS_CHOICES = [

        ('pending', 'Pending'),

        ('approved', 'Approved'),

        ('flagged', 'Flagged'),

        ('locked', 'Locked'),
    ]

    tenant = models.ForeignKey(

        Tenant,

        on_delete=models.CASCADE
    )

    facility = models.ForeignKey(

        Facility,

        on_delete=models.SET_NULL,

        null=True,

        blank=True
    )

    source_type = models.CharField(
        max_length=50
    )

    source_record_id = models.IntegerField(

        blank=True,

        null=True
    )

    activity_type = models.CharField(

        max_length=255,

        blank=True,

        null=True
    )

    activity_date = models.DateField(

        null=True,

        blank=True
    )

    original_quantity = (
        models.DecimalField(

            max_digits=15,

            decimal_places=2,

            default=0
        )
    )

    original_unit = models.CharField(

        max_length=50,

        blank=True,

        null=True
    )

    normalized_quantity = (
        models.DecimalField(

            max_digits=15,

            decimal_places=2,

            default=0
        )
    )

    normalized_unit = models.CharField(

        max_length=50,

        blank=True,

        null=True
    )

    scope = models.CharField(

        max_length=50,

        blank=True,

        null=True
    )

    emission_factor = (
        models.DecimalField(

            max_digits=15,

            decimal_places=4,

            default=0
        )
    )

    emission_factor_source = (
        models.CharField(

            max_length=255,

            blank=True,

            null=True
        )
    )

    co2e_kg = models.DecimalField(

        max_digits=15,

        decimal_places=2,

        default=0
    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='pending'
    )

    review_notes = models.TextField(

        blank=True,

        null=True
    )

    reviewer_email = models.EmailField(

        blank=True,

        null=True
    )

    reviewed_at = models.DateTimeField(

        null=True,

        blank=True
    )

    locked_at = models.DateTimeField(

        null=True,

        blank=True
    )

    source_file_name = models.CharField(

        max_length=500,

        blank=True,

        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f'{self.activity_type} - '
            f'{self.co2e_kg} kg'
        )