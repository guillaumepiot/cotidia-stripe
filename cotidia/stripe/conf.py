from django.conf import settings

from appconf import AppConf


class StripeConf(AppConf):
    SECRET_KEY = "****"
    END_POINT = "https://api.stripe.com"

    class Meta:
        prefix = 'stripe'
