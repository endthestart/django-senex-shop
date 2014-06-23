Senex Shop

1. Add the following applications to your settings.

    'senex_shop',
    'senex_shop.cart',
    'senex_shop.checkout',
    'senex_shop.contact',
    'senex_shop.core',
    'senex_shop.custom',
    'senex_shop.shipping',

2. Add the following URLs to your urls.py:

                       url(r'^contact/$', 'senex.views.contact', name='contact'),
                       url(r'^contact/thanks/$', 'senex.views.contact_thanks', name='contact_thanks'),
                       url(r'^checkout/', include('senex_shop.checkout.urls')),
                       url(r'^cart/', include('senex_shop.cart.urls')),
                       url(r'^shop/', include('senex_shop.urls')),


