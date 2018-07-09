from django.conf import settings

from appconf import AppConf


class StripeConf(AppConf):
    SECRET_KEY = "****"
    PUBLIC_KEY = "****"
    END_POINT = "https://api.stripe.com"
    DEFAULT_CURRENCY = "gbp"

    class Meta:
        prefix = 'stripe'
