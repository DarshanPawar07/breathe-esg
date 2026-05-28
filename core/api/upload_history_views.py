from rest_framework.views import APIView

from rest_framework.response import Response

from core.models import (

    SAPRecord,

    UtilityRecord,

    TravelRecord,
)


class UploadHistoryView(APIView):

    def get(self, request):

        uploads = []

        # SAP

        for item in (
            SAPRecord.objects.all()
            .order_by('-created_at')[:10]
        ):

            uploads.append({

                'id': item.id,

                'file_name': (
                    item.upload_id
                ),

                'source_type': 'SAP',

                'created_at': (
                    item.created_at
                ),

                'status': (
                    item.ingestion_status
                ),
            })

        # Utility

        for item in (
            UtilityRecord.objects.all()
            .order_by('-created_at')[:10]
        ):

            uploads.append({

                'id': item.id,

                'file_name': (
                    item.upload_id
                ),

                'source_type':
                    'Utility',

                'created_at': (
                    item.created_at
                ),

                'status': (
                    item.ingestion_status
                ),
            })

        # Travel

        for item in (
            TravelRecord.objects.all()
            .order_by('-created_at')[:10]
        ):

            uploads.append({

                'id': item.id,

                'file_name': (
                    item.upload_id
                ),

                'source_type':
                    'Travel',

                'created_at': (
                    item.created_at
                ),

                'status': (
                    item.ingestion_status
                ),
            })

        uploads = sorted(

            uploads,

            key=lambda x:
                x['created_at'],

            reverse=True
        )

        return Response(uploads)