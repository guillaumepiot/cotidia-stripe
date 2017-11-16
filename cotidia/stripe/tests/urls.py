from django.conf.urls import include, url

from cotidia.account.views.admin import dashboard

urlpatterns = [
    # url(
    #     r'^admin/stripe/',
    #     include(
    #         'cotidia.stripe.urls.admin',
    #         namespace="stripe-admin"
    #     )
    # ),
    url(
        r'^api/stripe/',
        include(
            'cotidia.stripe.urls.api',
            namespace="stripe-api"
        )
    ),
    # url(
    #     r'^stripe/',
    #     include(
    #         'cotidia.stripe.urls.public',
    #         namespace="stripe-public"
    #     )
    # ),
    url(
        r'^admin/account/',
        include(
            'cotidia.account.urls.admin',
            namespace="account-admin"
        )
    ),
    url(
        r'^admin/$',
        dashboard,
        name="dashboard"
    ),
]
