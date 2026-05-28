from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import EmissionRecord

from core.services.review.approve import (
    approve_emission_record
)

from core.services.review.flag import (
    flag_emission_record
)

from core.services.review.lock import (
    lock_emission_record
)


class ApproveEmissionView(APIView):

    def post(
        self,
        request,
        record_id
    ):

        reviewer_email = request.data.get(
            'reviewer_email',
            'analyst@breatheesg.com'
        )

        try:

            record = approve_emission_record(
                record_id=record_id,
                reviewer_email=reviewer_email
            )

            return Response({

                'success': True,

                'message': (
                    'Emission approved successfully'
                ),

                'record_id': record.id,

                'status': record.status,
            })

        except EmissionRecord.DoesNotExist:

            return Response({

                'success': False,

                'error': 'Record not found'
            },
            status=status.HTTP_404_NOT_FOUND
            )


class FlagEmissionView(APIView):

    def post(
        self,
        request,
        record_id
    ):

        reviewer_email = request.data.get(
            'reviewer_email',
            'analyst@breatheesg.com'
        )

        reason = request.data.get(
            'reason',
            'Suspicious values detected'
        )

        try:

            record = flag_emission_record(
                record_id=record_id,
                reviewer_email=reviewer_email,
                reason=reason
            )

            return Response({

                'success': True,

                'message': (
                    'Emission flagged successfully'
                ),

                'record_id': record.id,

                'status': record.status,
            })

        except EmissionRecord.DoesNotExist:

            return Response({

                'success': False,

                'error': 'Record not found'
            },
            status=status.HTTP_404_NOT_FOUND
            )


class LockEmissionView(APIView):

    def post(
        self,
        request,
        record_id
    ):

        try:

            record = lock_emission_record(
                record_id=record_id
            )

            return Response({

                'success': True,

                'message': (
                    'Emission locked successfully'
                ),

                'record_id': record.id,

                'status': record.status,
            })

        except EmissionRecord.DoesNotExist:

            return Response({

                'success': False,

                'error': 'Record not found'
            },
            status=status.HTTP_404_NOT_FOUND
            )