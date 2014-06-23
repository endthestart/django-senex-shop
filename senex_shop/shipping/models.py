from decimal import Decimal

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class ShippingMethod(models.Model):
    """
    Fields from shipping.base.ShippingMethod must be added here manually.
    """
    code = models.SlugField(
        _("slug"),
        max_length=128,
        unique=True,
    )
    name = models.CharField(
        _("name"),
        max_length=128,
        unique=True,
    )
    description = models.TextField(
        _("description"),
        blank=True,
    )

    _cart = None

    class Meta:
        abstract = True
        verbose_name = _("shipping method")
        verbose_name_plural = _("shipping methods")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name)
        super(ShippingMethod, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def set_cart(self, cart):
        self._cart = cart


class OrderAndItemsCharges(ShippingMethod):
    price_per_order = models.DecimalField(
        _("price per order"),
        decimal_places=2,
        max_digits=12,
        default=Decimal("0.00"),
    )
    price_per_item = models.DecimalField(
        _("price per item"),
        decimal_places=2,
        max_digits=12,
        default=Decimal("0.00"),
    )

    free_shipping_threshold = models.DecimalField(
        _("free shipping"),
        decimal_places=2,
        max_digits=12,
        default=Decimal("0.00"),
    )

    cart = None

    class Meta:
        verbose_name = _("order and item charge")
        verbose_name_plural = _("order and items charges")

    def set_cart(self, cart):
        self._cart = cart

    @property
    def charge_incl_tax(self):
        if self.free_shipping_threshold is not None and self._cart.total_incl_tax >= self.free_shipping_threshold:
            return Decimal("0.00")

        charge = self.price_per_order
        for line in self.cart.cartitem_set.all():
            charge += line.quantity * self.price_per_item
        return charge

    @property
    def charge_excl_tax(self):
        return self.charge_incl_tax


class WeightBased(ShippingMethod):
    upper_charge = models.DecimalField(
        _("upper charge"),
        decimal_places=2,
        max_digits=12,
        null=True,
        help_text=_("This is the charge when the weight of the cart is greater than all the weight bands."),
    )
    weight_attribute = 'weight'
    default_weight = models.DecimalField(
        _("default weight"),
        decimal_places=2,
        max_digits=12,
        default=Decimal("0.00"),
        help_text=_("Default product weight when no weight attribute is defined.")
    )

    class Meta:
        verbose_name = _("weight-based shipping method")
        verbose_name_plural = _("weight-based shipping methods")

    @property
    def charge_incl_tax(self):
        #TODO: Actually implement weight for products/carts
        return Decimal("0.00")

    @property
    def charge_excl_tax(self):
        return self.charge_incl_tax

    def get_band_for_weight(self, weight):
        bands = self.bands.filter(upper_limit__gte=weight).order_by('upper_limit')
        if not bands.count():
            # No band for this weight
            return None
        return bands[0]


class WeightBand(models.Model):
    method = models.ForeignKey(
        WeightBased,
        related_name='bands',
        verbose_name=_("method"),
    )
    upper_limit = models.FloatField(
        _("upper limit"),
        help_text=_("The upper limit of this weight band."),
    )
    charge = models.DecimalField(
        _("charge"),
        decimal_places=2,
        max_digits=12,
    )

    @property
    def weight_from(self):
        lower_bands = self.method.bands.filter(upper_limit__lt=self.upper_limit).order_by('-upper_limit')
        if not lower_bands:
            return Decimal("0.00")
        return lower_bands[0].upper_limit

    @property
    def weight_to(self):
        return self.upper_limit

    class Meta:
        ordering = ['upper_limit']
        verbose_name = _("weight band")
        verbose_name_plural = _("weight bands")

    def __unicode__(self):
        return _("charge for weight up to {0} units".format(self.upper_limit))
