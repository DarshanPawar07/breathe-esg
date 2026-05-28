import os

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from django.conf import settings

from core.models import Tenant

from core.services.ingestion.sap import (
    ingest_sap_csv
)

from core.services.ingestion.utility import (
    ingest_utility_csv
)

from core.services.ingestion.travel import (
    ingest_travel_csv
)


# ─────────────────────────────────────
# HELPERS
# ─────────────────────────────────────

def save_uploaded_file(

    uploaded_file,

    upload_dir,
):

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(

        upload_dir,

        uploaded_file.name
    )

    with open(

        file_path,

        'wb+'
    ) as destination:

        for chunk in (
            uploaded_file.chunks()
        ):

            destination.write(chunk)

    return file_path


# ─────────────────────────────────────
# SAP UPLOAD
# ─────────────────────────────────────

class UploadSAPView(APIView):

    def post(self, request):

        try:

            uploaded_file = request.FILES.get(
                'file'
            )

            tenant_id = request.data.get(
                'tenant_id'
            )

            if not uploaded_file:

                return Response(

                    {
                        'error':
                            'No file uploaded'
                    },

                    status=
                    status.HTTP_400_BAD_REQUEST
                )

            tenant = Tenant.objects.get(
                id=tenant_id
            )

            # Save file

            file_path = save_uploaded_file(

                uploaded_file,

                settings.SAP_UPLOAD_DIR
            )

            # Process CSV

            result = ingest_sap_csv(

                file_path=file_path,

                tenant=tenant,

                upload_id=
                    uploaded_file.name,
            )

            return Response({

                'message':
                    'SAP upload successful',

                'created':
                    result.get(
                        'created',
                        0
                    ),

                'failed':
                    result.get(
                        'failed',
                        0
                    ),

                'flagged':
                    result.get(
                        'flagged',
                        0
                    ),
            })

        except Exception as error:

            print(error)

            return Response(

                {
                    'error': str(error)
                },

                status=
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ─────────────────────────────────────
# UTILITY UPLOAD
# ─────────────────────────────────────

class UploadUtilityView(APIView):

    def post(self, request):

        try:

            uploaded_file = request.FILES.get(
                'file'
            )

            tenant_id = request.data.get(
                'tenant_id'
            )

            if not uploaded_file:

                return Response(

                    {
                        'error':
                            'No file uploaded'
                    },

                    status=
                    status.HTTP_400_BAD_REQUEST
                )

            tenant = Tenant.objects.get(
                id=tenant_id
            )

            # Save file

            file_path = save_uploaded_file(

                uploaded_file,

                settings.UTILITY_UPLOAD_DIR
            )

            # Process CSV

            result = ingest_utility_csv(

                file_path=file_path,

                tenant=tenant,

                upload_id=
                    uploaded_file.name,
            )

            return Response({

                'message':
                    'Utility upload successful',

                'created':
                    result.get(
                        'created',
                        0
                    ),

                'failed':
                    result.get(
                        'failed',
                        0
                    ),

                'flagged':
                    result.get(
                        'flagged',
                        0
                    ),
            })

        except Exception as error:

            print(error)

            return Response(

                {
                    'error': str(error)
                },

                status=
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ─────────────────────────────────────
# TRAVEL UPLOAD
# ─────────────────────────────────────

class UploadTravelView(APIView):

    def post(self, request):

        try:

            uploaded_file = request.FILES.get(
                'file'
            )

            tenant_id = request.data.get(
                'tenant_id'
            )

            if not uploaded_file:

                return Response(

                    {
                        'error':
                            'No file uploaded'
                    },

                    status=
                    status.HTTP_400_BAD_REQUEST
                )

            tenant = Tenant.objects.get(
                id=tenant_id
            )

            # Save file

            file_path = save_uploaded_file(

                uploaded_file,

                settings.TRAVEL_UPLOAD_DIR
            )

            # Process CSV

            result = ingest_travel_csv(

                file_path=file_path,

                tenant=tenant,

                upload_id=
                    uploaded_file.name,
            )

            return Response({

                'message':
                    'Travel upload successful',

                'created':
                    result.get(
                        'created',
                        0
                    ),

                'failed':
                    result.get(
                        'failed',
                        0
                    ),

                'flagged':
                    result.get(
                        'flagged',
                        0
                    ),
            })

        except Exception as error:

            print(error)

            return Response(

                {
                    'error': str(error)
                },

                status=
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )