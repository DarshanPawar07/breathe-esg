from django.core.management.base import (
    BaseCommand
)

from core.models import (
    Tenant,
    Facility,
)


class Command(BaseCommand):

    help = (
        'Seed initial tenant and facilities'
    )

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING(
                '\nSeeding ESG demo data...\n'
            )
        )

        # ─────────────────────────────
        # TENANT
        # ─────────────────────────────

        tenant, created = (
            Tenant.objects.get_or_create(

                name='Tata Motors'
            )
        )

        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    'Created tenant: Tata Motors'
                )
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    'Tenant already exists'
                )
            )

        # ─────────────────────────────
        # FACILITIES
        # ─────────────────────────────

        facilities = [

            {
                'facility_code': 'MU01',

                'facility_name': (
                    'Mumbai Plant'
                ),

                'facility_type': (
                    'manufacturing'
                ),

                'city': 'Mumbai',

                'country': 'India',
            },

            {
                'facility_code': 'PU02',

                'facility_name': (
                    'Pune Assembly'
                ),

                'facility_type': (
                    'manufacturing'
                ),

                'city': 'Pune',

                'country': 'India',
            },

            {
                'facility_code': 'HQ01',

                'facility_name': (
                    'HQ Mumbai Office'
                ),

                'facility_type': (
                    'office'
                ),

                'city': 'Mumbai',

                'country': 'India',
            },

            {
                'facility_code': 'BLR01',

                'facility_name': (
                    'Bangalore Office'
                ),

                'facility_type': (
                    'office'
                ),

                'city': 'Bangalore',

                'country': 'India',
            },
        ]

        created_count = 0

        for facility_data in facilities:

            facility, was_created = (
                Facility.objects.get_or_create(

                    tenant=tenant,

                    facility_code=(
                        facility_data[
                            'facility_code'
                        ]
                    ),

                    defaults={

                        'facility_name': (
                            facility_data[
                                'facility_name'
                            ]
                        ),

                        'facility_type': (
                            facility_data[
                                'facility_type'
                            ]
                        ),

                        'city': (
                            facility_data[
                                'city'
                            ]
                        ),

                        'country': (
                            facility_data[
                                'country'
                            ]
                        ),
                    }
                )
            )

            if was_created:

                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(

                        f'Created facility: '
                        f'{facility.facility_name}'
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(

                        f'Facility already exists: '
                        f'{facility.facility_name}'
                    )
                )

        # ─────────────────────────────
        # SUMMARY
        # ─────────────────────────────

        self.stdout.write(
            self.style.SUCCESS(
                '\nSeed completed successfully.\n'
            )
        )

        self.stdout.write(

            f'Tenant: {tenant.name}\n'

            f'Facilities created: '
            f'{created_count}\n'
        )