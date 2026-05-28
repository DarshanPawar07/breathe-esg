# test_emissions.py
from django.test import TestCase

from core.services.emissions.calculations import (
    calculate_fuel_emissions
)


class EmissionCalculationTestCase(TestCase):

    def test_fuel_emission_calculation(self):

        result = calculate_fuel_emissions(
            100
        )

        self.assertEqual(
            round(result['co2e_kg'], 2),
            268
        )