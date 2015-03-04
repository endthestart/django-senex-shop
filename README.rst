Requirements

Requires a Stripe.js account: Currently senex shop only supports Stripe as a payment backend. As such the setting is permanently required. Once more payment backends are added this will be configurable in the admin.

Add the following to your requirements.txt:

Django==1.7.5
django-braces==1.4.0
django-model-utils==2.0.3
easy-thumbnails==2.2
pytz==2014.4

django-senex-shop==0.2.2

Configure your Settings:

MIDDLEWARE_CLASSES = (
    '...',
    'senex_shop.cart.middleware.CartMiddleware',
    '...',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    '...',
    'senex_shop.core.context_processors.get_default_shop',
    '...',
)

INSTALLED_APPS = (
    '...',
    'localflavor',
    'easy_thumbnails',
    'senex_shop',
    'senex_shop.cart',
    'senex_shop.contact',
    'senex_shop.checkout',
    'senex_shop.core',
    'senex_shop.custom',
    'senex_shop.discounts',
    'senex_shop.news',
    'senex_shop.shipping',
)


########## THUMBNAIL CONFIGURATION
# See: http://easy-thumbnails.readthedocs.org/en/latest/ref/settings/
THUMBNAIL_BASEDIR = 'thumbs'
########## END THUMBNAIL CONFIGURATION




from os import environ


########## STRIPE CONFIGURATION
# See: http://django-stripe-payments.readthedocs.org/en/latest/installation.html
STRIPE_PUBLIC_KEY = environ.get("STRIPE_PUBLIC_KEY", "pk_test_BnKaAmgD81hWGi1F1suzPmX6")
STRIPE_SECRET_KEY = environ.get("STRIPE_SECRET_KEY", "sk_test_x1CjT9YMoj30rlpg50CnmD8A")
########## END STRIPE


Run ./manage.py migrate
Run ./manage.py createsuperuser


urls.py


url(r'^checkout/', include('senex_shop.checkout.urls')),
url(r'^cart/', include('senex_shop.cart.urls')),
url(r'^shop/', include('senex_shop.urls')),
url(r'^account/', include('custom_auth.urls')),