from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import (
    EmissionRecord,
    Facility,
    Tenant,
)


class DashboardSummaryView(APIView):

    def get(self, request):

        tenant_id = request.GET.get(
            'tenant'
        )

        facility_id = request.GET.get(
            'facility'
        )

        queryset = EmissionRecord.objects.all()

        # ─────────────────────────────
        # FILTERING
        # ─────────────────────────────

        if tenant_id:

            queryset = queryset.filter(
                tenant_id=tenant_id
            )

        if facility_id:

            queryset = queryset.filter(
                facility_id=facility_id
            )

        # ─────────────────────────────
        # COUNTS
        # ─────────────────────────────

        total_rows = queryset.count()

        pending_count = queryset.filter(
            status='pending'
        ).count()

        approved_count = queryset.filter(
            status='approved'
        ).count()

        flagged_count = queryset.filter(
            status='flagged'
        ).count()

        locked_count = queryset.filter(
            status='locked'
        ).count()

        # ─────────────────────────────
        # EMISSION TOTALS
        # ─────────────────────────────

        scope_1_total = queryset.filter(
            scope='Scope 1'
        ).aggregate(
            total=Sum('co2e_kg')
        )['total'] or 0

        scope_2_total = queryset.filter(
            scope='Scope 2'
        ).aggregate(
            total=Sum('co2e_kg')
        )['total'] or 0

        scope_3_total = queryset.filter(
            scope='Scope 3'
        ).aggregate(
            total=Sum('co2e_kg')
        )['total'] or 0

        # ─────────────────────────────
        # FILTER OPTIONS
        # ─────────────────────────────

        facilities = Facility.objects.all()

        tenants = Tenant.objects.all()

        return Response({

            'summary': {

                'total_rows': total_rows,

                'pending': pending_count,

                'approved': approved_count,

                'flagged': flagged_count,

                'locked': locked_count,

                'scope_1_total': float(
                    scope_1_total
                ),

                'scope_2_total': float(
                    scope_2_total
                ),

                'scope_3_total': float(
                    scope_3_total
                ),
            },

            'filters': {

                'facilities': [

                    {
                        'id': facility.id,

                        'facility_code': (
                            facility.facility_code
                        ),

                        'facility_name': (
                            facility.facility_name
                        ),
                    }

                    for facility in facilities
                ],

                'tenants': [

                    {
                        'id': tenant.id,

                        'name': tenant.name,
                    }

                    for tenant in tenants
                ],
            }
        })