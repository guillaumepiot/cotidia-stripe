from django.contrib.sites.models import Site
from django.conf import settings


def stripe_settings(request):
    return {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'STRIPE_END_POINT': settings.STRIPE_END_POINT,
        'STRIPE_DEFAULT_CURRENCY': settings.STRIPE_DEFAULT_CURRENCY
    }
