from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cotidia.stripe.conf import settings
from cotidia.stripe.utils import (
    stripe_customer, stripe_subscription, stripe_token
)
from cotidia.stripe.serializers import (
    SubscribeSerializer
)
from cotidia.stripe.models import Customer, Subscription


class Subscribe(APIView):
    """Handle subscription."""

    # authentication_classes = ()
    # permission_classes = ()
    serializer_class = SubscribeSerializer

    @transaction.atomic
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            customer_description = \
                f"{request.user.first_name} {request.user.last_name} <{request.user.email}>"

            # Check if the customer already exist
            try:
                customer_obj = Customer.objects.get(user=request.user)
                customer = stripe_customer.retrieve(customer_obj.stripe_id)
            except Customer.DoesNotExist:
                customer = stripe_customer.create(
                    description=customer_description,
                )
                customer_obj = Customer.objects.create(
                    user=request.user,
                    description=customer_description,
                    stripe_id=customer["id"]
                )

            # Check if the customer has a payment source, if not create a card
            # token
            if len(customer.sources.all(object="card")["data"]) == 0:
                token = stripe_token.create(
                    card={
                        "number": serializer.data["card_number"],
                        "exp_month": serializer.data["card_exp_month"],
                        "exp_year": serializer.data["card_exp_year"],
                        "cvc": serializer.data["card_cvc"]
                    }
                )
                customer.sources.create(source=token["id"])

            # Check if the customer has a subscription already
            try:
                subscription_obj = Subscription.objects.get(
                    customer=customer_obj
                )

                # Update the Stripe subscription
                subscription = stripe_subscription.retrieve(subscription_obj.stripe_id)
                subscription.items = [
                    {
                        "plan": serializer.data["plan_id"],
                    },
                ]
                subscription.save()

                # Update the subscription object
                subscription_obj.plan_id = serializer.data["plan_id"],
                subscription_obj.current_period_start = subscription["current_period_start"]
                subscription_obj.current_period_end = subscription["current_period_end"]
                subscription_obj.cancel_at_period_end = subscription["cancel_at_period_end"]
                subscription_obj.canceled_at = subscription["canceled_at"]
                subscription_obj.save()

            except Subscription.DoesNotExist:
                # Create the Stripe subscription
                subscription = stripe_subscription.create(
                    customer=customer["id"],
                    items=[
                        {
                            "plan": serializer.data["plan_id"],
                        },
                    ])

                # Create the subscription object
                Subscription.objects.create(
                    customer=customer_obj,
                    stripe_id=subscription["id"],
                    plan_id=serializer.data["plan_id"],
                    current_period_start=subscription["current_period_start"],
                    current_period_end=subscription["current_period_end"],
                    cancel_at_period_end=subscription["cancel_at_period_end"],
                    canceled_at=subscription["canceled_at"]
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
