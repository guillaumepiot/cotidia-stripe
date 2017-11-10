# Cotidia stripe

A plugin to manage payments and subscription using the Stripe API.

```console
$ pip install -e git+git@code.cotidia.com:cotidia/stripe.git#egg=cotidia-stripe
```

## Settings

Add `cotidia.stripe` to your INSTALLED_APPS:

```python
INSTALLED_APPS=[
    ...
    "cotidia.stripe",

]
```

```python
STRIPE_SECRET_KEY = "****"
```

## URLs

Add `stripe-admin`, `stripe-api` and `stripe-public` to the URLs:

```python
urlpatterns = [
    url(
        r'^admin/stripe/',
        include('cotidia.stripe.urls.admin', namespace="stripe-admin")
    ),
    url(
        r'^api/stripe/',
        include('cotidia.stripe.urls.api', namespace="stripe-api")
    ),
    url(
        r'^public/stripe/',
        include('cotidia.stripe.urls.public', namespace="stripe-public")
    ),
]
```

## Test

Run the test from a virtual environment.

```console
$ python runtests.py
```
