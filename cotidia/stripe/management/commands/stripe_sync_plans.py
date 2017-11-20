from django.core.management.base import BaseCommand

from pinax.stripe.actions import plans


class Command(BaseCommand):
    help = 'Sync Stripe plans to database.'

    def handle(self, *args, **options):
        plans.sync_plans()
