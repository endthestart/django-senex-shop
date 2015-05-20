from decimal import Decimal

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from senex_shop.core.models import Shop


class ShippingModule(models.Model):
    shop = models.OneToOneField(
        Shop,
        related_name='shipping_module',
    )
    price_per_order = models.DecimalField(
        _(u"price per order"),
        decimal_places=2,
        max_digits=12,
        default=Decimal("0.00"),
    )
    price_per_item = models.DecimalField(
        _(u"price per item"),
        decimal_places=2,
        max_digits=12,
        default=Decimal("0.00"),
    )
    free_shipping_threshold = models.DecimalField(
        _(u"free shipping threshold"),
        decimal_places=2,
        max_digits=12,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _(u"shipping module")
        verbose_name_plural = _(u"shipping modules")

    def __unicode__(self):
        return u"{0} Shipping Module".format(self.shop)

    def calculate(self, cart):
        if self.free_shipping_threshold is not None and cart.subtotal >= self.free_shipping_threshold:
            return Decimal("0.00")

        charge = Decimal("0.00")
        if cart.num_items > 0:
            charge = self.price_per_order
            for item in cart.cartitem_set.all():
                if item.product.shipping_required:
                    charge += item.quantity * self.price_per_item

        return charge