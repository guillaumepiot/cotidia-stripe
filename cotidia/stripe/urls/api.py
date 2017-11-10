from django.conf.urls import url

from cotidia.stripe.views import api

ure = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(
        r'^subscribe$',
        api.Subscribe.as_view(),
        name="subscribe"
    ),
    # url(
    #     r'^subscribe/update$',
    #     api.Subscribe.as_view(),
    #     {
    #         "serializer_class": SubscribeUpdateSerializer
    #     },
    #     name="subscribe-update",
    # ),
]
