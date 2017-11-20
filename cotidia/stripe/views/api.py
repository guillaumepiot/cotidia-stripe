import stripe

from django.db import transaction
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cotidia.stripe.utils import (
    stripe_customer, stripe_subscription, stripe_token
)
from cotidia.stripe.serializers import (
    SubscriptionCreateSerializer,
    SubscriptionUpdateSerializer
)
from pinax.stripe.actions import customers, subscriptions, sources
from pinax.stripe.models import Customer, Subscription


class SubscriptionCreate(APIView):
    """Create a new subscription."""

    # authentication_classes = ()
    # permission_classes = ()
    serializer_class = SubscriptionCreateSerializer

    @transaction.atomic
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            # Get or create the customer
            try:
                customer = Customer.objects.get(user=request.user)
            except Customer.DoesNotExist:
                customer = customers.create(
                    user=request.user
                )

            if not customers.can_charge(customer):

                if serializer.data["card_number"]:
                    try:
                        token = stripe_token.create(
                            card={
                                "number": serializer.data["card_number"],
                                "exp_month": serializer.data["card_exp_month"],
                                "exp_year": serializer.data["card_exp_year"],
                                "cvc": serializer.data["card_cvc"]
                            }
                        )
                    except stripe.error.CardError as e:
                        data = {
                            "non_field_errors": [e.json_body["error"]["message"]]
                        }
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        sources.create_card(customer, token)
                    except stripe.error.CardError as e:
                        data = {
                            "non_field_errors": [e.json_body["error"]["message"]]
                        }
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)

            try:
                subscriptions.create(
                    customer=customer,
                    plan=serializer.data["plan_id"]
                )
            except stripe.error.InvalidRequestError as e:
                data = {
                    "non_field_errors": [e.json_body["error"]["message"]]
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            subscription = SubscriptionUpdateSerializer(
                data={"plan_id": serializer.data["plan_id"]}
            )
            subscription.is_valid()

            return Response(subscription.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionUpdate(APIView):
    """Update a subscription."""

    # authentication_classes = ()
    # permission_classes = ()
    serializer_class = SubscriptionUpdateSerializer

    @transaction.atomic
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            customer = Customer.objects.get(user=request.user)
            subscription = Subscription.objects.get(customer=customer)

            subscriptions.update(
                subscription=subscription,
                plan=serializer.data["plan_id"]
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
