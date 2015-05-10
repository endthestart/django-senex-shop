from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from .models import ShippingMethod


class Free(ShippingMethod):
    code = 'free-shipping'
    name = _(u"free shipping")

    def calculate(self, cart):
        return Decimal("0.00")


class NoShippingRequired(Free):
    """
    This is a special shipping method that indicates that no shipping is
    actually required (eg for digital goods).
    """
    code = 'no-shipping-required'
    name = _(u"no shipping required")


class FixedPrice(ShippingMethod):
    code = 'fixed-price-shipping'
    name = _(u"fixed price shipping")

    def __init__(self, charge_excl_tax, charge_incl_tax=None):
        self.charge_excl_tax = charge_excl_tax
        if charge_incl_tax is not None:
            self.charge_incl_tax = charge_incl_tax
            self.is_tax_known = True