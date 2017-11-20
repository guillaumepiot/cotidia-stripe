import json
import datetime

from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.renderers import JSONRenderer

from cotidia.account import fixtures
from cotidia.account.doc import Doc
from cotidia.stripe.utils import stripe_token

from pinax.stripe.models import Customer, Subscription
from pinax.stripe.actions import subscriptions, plans, customers, sources


class SubscribeAPITests(APITestCase):

    display_doc = True

    @fixtures.normal_user
    def setUp(self):
        self.doc = Doc()

        next_year = datetime.datetime.now() + datetime.timedelta(days=365)
        next_year = next_year.strftime("%Y")

        self.card = {
            'card_number': "4242 4242 4242 4242",
            'card_exp_month': 12,
            'card_exp_year': next_year,
            'card_cvc': "123"
        }

    def jsonify(self, data):
        """Make clean JSON for doc output."""

        return json.loads(JSONRenderer().render(data).decode("utf-8"))

    def test_subscribe_create(self):
        """Test create a subscription."""

        plans.sync_plans()

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key
        )

        data = {
            'plan_id': "MF-MONTHLY",

        }
        data.update(self.card)

        url = reverse('stripe-api:subscription-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the customer was created and has a subscription
        customer = Customer.objects.get(user=self.normal_user)
        self.assertTrue(subscriptions.has_active_subscription(customer))

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Subscribe",
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
                'response_status': response.status_code,
                'description': (
                    "Subscribe to a give plan with card details."
                )
            }
            self.doc.display_section(content)

    def test_subscribe_update(self):
        """Test update a subscription."""

        plans.sync_plans()

        customer = customers.create(
            user=self.normal_user
        )
        token = stripe_token.create(
            card={
                "number": self.card["card_number"],
                "exp_month": self.card["card_exp_month"],
                "exp_year": self.card["card_exp_year"],
                "cvc": self.card["card_cvc"]
            }
        )
        sources.create_card(customer, token)
        subscriptions.create(
            customer=customer,
            plan="MF-MONTHLY"
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key
        )

        data = {
            'plan_id': "MF-YEARLY",
        }

        url = reverse('stripe-api:subscription-update')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the customer was created and has a subscription
        customer = Customer.objects.get(user=self.normal_user)
        subscription = Subscription.objects.get(customer=customer)
        self.assertTrue(subscription.plan_id, data['plan_id'])

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Subscribe",
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
                'response_status': response.status_code,
                'description': (
                    "Subscribe to a give plan with card details."
                )
            }
            self.doc.display_section(content)

    def test_subscription_valid(self):
        # @TODO: test that the plan id is valid
        pass
