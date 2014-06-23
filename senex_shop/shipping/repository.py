from decimal import Decimal

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

import methods


class Repository(object):
    """
    Repository class responsible for returning ShippingMethod objects for a given user, cart...
    """
    methods = (methods.Free(),)

    def get_shipping_methods(self, user, cart, shipping_address=None, request=None, **kwargs):
        return self.prime_methods(cart, self.methods)

    def get_default_shipping_method(self, user, cart, shipping_address=None, request=None, **kwargs):
        shipping_methods = self.get_shipping_methods(user, cart, shipping_address, request, **kwargs)
        if len(shipping_methods) == 0:
            raise ImproperlyConfigured(
                _("You need to define a shipping method.")
            )
        return min(shipping_methods, key=lambda method: method.charge_excl_tax)

    def prime_methods(self, cart, methods):
        return [self.prime_method(cart, method) for method in methods]

    def prime_method(self, cart, method):
        method.set_cart(cart)
        return method

    def find_by_code(self, code, cart):
        for method in self.methods:
            if method.code == code:
                return self.prime_method(cart, method)

        if code == methods.NoShippingRequired.code:
            return self.prime_method(cart, methods.NoShippingRequired())
