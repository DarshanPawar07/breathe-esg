from django.urls import path

# Dashboard APIs
from core.api.dashboard_views import (
    DashboardSummaryView
)

# Emission APIs
from core.api.emission_views import (

    EmissionRecordListView,

    PendingEmissionRecordsView,

    ApprovedEmissionRecordsView,
)

# Review APIs
from core.api.review_views import (

    ApproveEmissionView,

    FlagEmissionView,

    LockEmissionView,
)

# Upload APIs
from core.api.upload_views import (

    UploadSAPView,

    UploadUtilityView,

    UploadTravelView,
)

# Upload History
from core.api.upload_history_views import (
    UploadHistoryView
)


urlpatterns = [

    # ─────────────────────────────
    # DASHBOARD
    # ─────────────────────────────

    path(

        'dashboard/',

        DashboardSummaryView.as_view(),

        name='dashboard-summary'
    ),

    # ─────────────────────────────
    # EMISSION RECORDS
    # ─────────────────────────────

    path(

        'emission-records/',

        EmissionRecordListView.as_view(),

        name='emission-records'
    ),

    path(

        'emission-records/pending/',

        PendingEmissionRecordsView.as_view(),

        name='pending-emission-records'
    ),

    path(

        'emission-records/approved/',

        ApprovedEmissionRecordsView.as_view(),

        name='approved-emission-records'
    ),

    # ─────────────────────────────
    # REVIEW ACTIONS
    # ─────────────────────────────

    path(

        'review/<int:record_id>/approve/',

        ApproveEmissionView.as_view(),

        name='approve-emission'
    ),

    path(

        'review/<int:record_id>/flag/',

        FlagEmissionView.as_view(),

        name='flag-emission'
    ),

    path(

        'review/<int:record_id>/lock/',

        LockEmissionView.as_view(),

        name='lock-emission'
    ),

    # ─────────────────────────────
    # FILE UPLOADS
    # ─────────────────────────────

    path(

        'upload/sap/',

        UploadSAPView.as_view(),

        name='upload-sap'
    ),

    path(

        'upload/utility/',

        UploadUtilityView.as_view(),

        name='upload-utility'
    ),

    path(

        'upload/travel/',

        UploadTravelView.as_view(),

        name='upload-travel'
    ),

    # ─────────────────────────────
    # UPLOAD HISTORY
    # ─────────────────────────────

    path(

        'upload-history/',

        UploadHistoryView.as_view(),

        name='upload-history'
    ),
]