from django.apps import AppConfig


class StripeConfig(AppConfig):
    name = "cotidia.stripe"
    label = "stripe"

    def ready(self):
        import cotidia.stripe.signals
