import stripe

from cotidia.stripe.conf import settings


def stripe_customer():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Customer

stripe_customer = stripe_customer()


def stripe_subscription():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Subscription

stripe_subscription = stripe_subscription()


def stripe_token():
    stripe.api_key = settings.PINAX_STRIPE_SECRET_KEY
    return stripe.Token

stripe_token = stripe_token()
