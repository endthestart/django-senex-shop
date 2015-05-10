from decimal import Decimal

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

import methods as shipping_methods


class Repository(object):
    """
    Repository class responsible for returning ShippingMethod objects for a given user, cart...
    """
    methods = (shipping_methods.Free(),)

    def get_shipping_methods(self, user, cart, shipping_address=None, request=None, **kwargs):
        if not cart.is_shipping_required():
            return [shipping_methods.NoShippingRequired()]

        methods = self.get_available_shipping_methods(cart=cart, shipping_address=shipping_address, **kwargs)

        return methods

    def get_available_shipping_methods(self, car, shipping_address=None, **kwargs):
        return self.methods

    def get_default_shipping_method(self, user, cart, shipping_address=None, **kwargs):
        shipping_methods = self.get_shipping_methods(user, cart, shipping_address=shipping_address, **kwargs)
        if len(shipping_methods) == 0:
            raise ImproperlyConfigured(
                _("You need to define a shipping method.")
            )
        return shipping_methods[0]
