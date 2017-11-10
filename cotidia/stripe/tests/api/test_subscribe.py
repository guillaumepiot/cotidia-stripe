import json
import datetime

from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.renderers import JSONRenderer

from cotidia.account import fixtures
from cotidia.account.doc import Doc


class SubscribeAPITests(APITestCase):

    display_doc = True

    @fixtures.normal_user
    def setUp(self):
        self.doc = Doc()

    def jsonify(self, data):
        """Make clean JSON for doc output."""

        return json.loads(JSONRenderer().render(data).decode("utf-8"))

    def test_update_details(self):
        """Test plan subscription."""

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key
        )

        next_year = datetime.datetime.now() + datetime.timedelta(days=365)
        next_year = next_year.strftime("%Y")

        data = {
            'plan_id': "MF-MONTHLY",
            'card_number': "4242 4242 4242 4242",
            'card_exp_month': 12,
            'card_exp_year': next_year,
            'card_cvc': "123"
        }
        url = reverse('stripe-api:subscribe')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # With authentication
        # self.client.credentials(
        #     HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)

        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEquals(response.data['first_name'], "Jack")
        # self.assertEquals(response.data['last_name'], "Green")
        # self.assertEquals(response.data['email'], "john@green.com")

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
