from django.core.management.base import BaseCommand
from products.models import Rental
from datetime import date

class Command(BaseCommand):
    help = 'Désactive les locations expirées (is_active = False)'

    def handle(self, *args, **kwargs):
        expired_rentals = Rental.objects.filter(is_active=True, end_date__lt=date.today())
        count = expired_rentals.update(is_active=False)
        self.stdout.write(self.style.SUCCESS(f'{count} location(s) désactivée(s).'))
