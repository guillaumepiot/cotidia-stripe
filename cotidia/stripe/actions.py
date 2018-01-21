import stripe

from pinax.stripe.models import Customer
from pinax.stripe.actions import sources, charges

from cotidia.stripe.conf import settings
from cotidia.stripe.utils import (
    stripe_customer, stripe_token, stripe_source, stripe_charge
)


def charge(
        amount,
        card_number,
        card_exp_month,
        card_exp_year,
        card_cvc,
        currency=settings.STRIPE_DEFAULT_CURRENCY,
        description=None,
        user=None):

    # Create a customer reference if we have a user
    if user:
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(
                user=user,
                currency=currency
            )
    else:
        customer = None

    # Request a card token from Stripe
    try:
        token = stripe_token.create(
            card={
                "number": card_number,
                "exp_month": card_exp_month,
                "exp_year": card_exp_year,
                "cvc": card_cvc
            }
        )
    except stripe.error.CardError as e:
        data = {
            "non_field_errors": [e.json_body["error"]["message"]]
        }
        return data

    if customer:
        # Add that card as a source and register it with the customer
        try:
            sources.create_card(customer, token)
        except stripe.error.CardError as e:
            data = {
                "non_field_errors": [e.json_body["error"]["message"]]
            }
            return data
    else:
        try:
            source = stripe_source.create(
                type='card',
                token=token
            )
        except stripe.error.CardError as e:
            data = {
                "non_field_errors": [e.json_body["error"]["message"]]
            }
            return data

    # Charge the source with the right amount
    try:
        amount_int = int(amount * 100)
        if customer:
            charges.create(
                customer=customer,
                amount=amount_int,
                description=description
            )
        else:
            stripe_charge.create(
                source=source,
                amount=amount_int,
                currency=currency,
                description=description
            )
    except stripe.error.CardError as e:
        data = {
            "non_field_errors": [e.json_body["error"]["message"]]
        }
        return data

    return True
