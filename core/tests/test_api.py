# test_api.py
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Tenant


class APITestCase(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.tenant = Tenant.objects.create(
            name='API Test Tenant'
        )

    def test_health_check(self):

        response = self.client.get('/api/')

        self.assertEqual(
            response.status_code,
            200
        )