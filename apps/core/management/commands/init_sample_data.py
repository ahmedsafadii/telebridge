"""
Management command to initialize sample data for TeleBridge.
"""

from django.core.management.base import BaseCommand
from apps.core.models import Country
from apps.accounts.models import TelegramAccount


class Command(BaseCommand):
    help = 'Initialize sample data for TeleBridge project'

    def handle(self, *args, **options):
        self.stdout.write('Initializing sample data...')
        
        # Create sample countries
        countries_data = [
            {'name': 'Palestine', 'code': 'PSE', 'phone_code': '970'},
            {'name': 'United States', 'code': 'USA', 'phone_code': '1'},
            {'name': 'United Kingdom', 'code': 'GBR', 'phone_code': '44'},
            {'name': 'Germany', 'code': 'DEU', 'phone_code': '49'},
            {'name': 'France', 'code': 'FRA', 'phone_code': '33'},
        ]
        
        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults=country_data
            )
            if created:
                self.stdout.write(f'Created country: {country.name}')
            else:
                self.stdout.write(f'Country already exists: {country.name}')
        
        # Create sample Telegram account (you'll need to update with real API credentials)
        sample_account_data = {
            'name': 'Ahmed Telegram',
            'api_id': '22326188',  # Replace with real API ID
            'api_hash': '039fd0998b38661a863a3a9bfacdd874',  # Replace with real API hash
            'phone_number': '+905523239456',  # Replace with real phone number
            'country': Country.objects.get(code='PSE'),
            'is_active': True,
        }
        
        account, created = TelegramAccount.objects.get_or_create(
            phone_number=sample_account_data['phone_number'],
            defaults=sample_account_data
        )
        
        if created:
            self.stdout.write(f'Created Telegram account: {account.name}')
        else:
            self.stdout.write(f'Telegram account already exists: {account.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Sample data initialization completed successfully!')
        )
