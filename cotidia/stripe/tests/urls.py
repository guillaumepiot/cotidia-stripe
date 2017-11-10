from django.conf.urls import include, url

from cotidia.account.views.admin import dashboard

urlpatterns = [
    url(
        r'^admin/testimonial/',
        include(
            'cotidia.testimonial.urls.admin',
            namespace="testimonial-admin"
        )
    ),
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
