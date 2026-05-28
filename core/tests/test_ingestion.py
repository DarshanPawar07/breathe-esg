# test_ingestion.py
from django.test import TestCase

from core.models import Tenant


class IngestionTestCase(TestCase):

    def setUp(self):

        self.tenant = Tenant.objects.create(
            name='Test Tenant'
        )

    def test_tenant_created(self):

        self.assertEqual(
            self.tenant.name,
            'Test Tenant'
        )