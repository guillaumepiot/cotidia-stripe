from django.conf.urls import url

from cotidia.stripe.views import api

ure = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


app_name = 'cotidia.stripe'

urlpatterns = [
    url(
        r'^subscription/create$',
        api.SubscriptionCreate.as_view(),
        name="subscription-create"
    ),
    url(
        r'^subscription/update$',
        api.SubscriptionUpdate.as_view(),
        name="subscription-update"
    ),
]
