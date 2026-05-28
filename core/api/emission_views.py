from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import EmissionRecord

from core.serializers import (
    EmissionRecordSerializer
)


class EmissionRecordListView(APIView):

    def get(self, request):

        queryset = (
            EmissionRecord.objects.select_related(
                'facility',
                'tenant'
            )
            .all()
            .order_by('-created_at')
        )

        # ─────────────────────────────
        # FILTERS
        # ─────────────────────────────

        status_filter = request.GET.get(
            'status'
        )

        facility_id = request.GET.get(
            'facility'
        )

        source_type = request.GET.get(
            'source_type'
        )

        scope = request.GET.get(
            'scope'
        )

        if status_filter:

            queryset = queryset.filter(
                status=status_filter
            )

        if facility_id:

            queryset = queryset.filter(
                facility_id=facility_id
            )

        if source_type:

            queryset = queryset.filter(
                source_type=source_type
            )

        if scope:

            queryset = queryset.filter(
                scope=scope
            )

        serializer = (
            EmissionRecordSerializer(
                queryset,
                many=True
            )
        )

        return Response(serializer.data)


class PendingEmissionRecordsView(APIView):

    def get(self, request):

        queryset = (
            EmissionRecord.objects.filter(
                status='pending'
            )
            .order_by('-created_at')
        )

        serializer = (
            EmissionRecordSerializer(
                queryset,
                many=True
            )
        )

        return Response(serializer.data)


class ApprovedEmissionRecordsView(APIView):

    def get(self, request):

        queryset = (
            EmissionRecord.objects.filter(
                status='approved'
            )
            .order_by('-created_at')
        )

        serializer = (
            EmissionRecordSerializer(
                queryset,
                many=True
            )
        )

        return Response(serializer.data)