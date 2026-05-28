# test_validation.py
from django.test import TestCase

from core.services.validation.suspicious_rules import (
    is_suspicious_fuel_quantity
)


class ValidationTestCase(TestCase):

    def test_suspicious_quantity(self):

        result = is_suspicious_fuel_quantity(
            200000
        )

        self.assertTrue(result)