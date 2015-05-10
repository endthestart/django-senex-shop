from decimal import Decimal

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class ShippingMethod(models.Model):
    """
    Fields from shipping.base.ShippingMethod must be added here manually.
    """
    code = models.SlugField(
        _(u"slug"),
        max_length=128,
        unique=True,
    )
    name = models.CharField(
        _(u"name"),
        max_length=128,
        unique=True,
    )
    description = models.TextField(
        _(u"description"),
        blank=True,
    )
    priority = models.IntegerField(
        _(u"priority"),
        default=0,
    )
    active = models.BooleanField(
        _(u"active"),
        default=False,
    )

    class Meta:
        abstract = True
        verbose_name = _(u"shipping method")
        verbose_name_plural = _(u"shipping methods")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name)
        super(ShippingMethod, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class WeightBased(ShippingMethod):
    weight_attribute = 'weight'
    upper_charge = models.DecimalField(
        _(u"upper charge"),
        decimal_places=2,
        max_digits=12,
        null=True,
        help_text=_(u"This is the charge when the weight of the cart is greater than all the weight bands."),
        )
    default_weight = models.DecimalField(
        _(u"default weight"),
        decimal_places=2,
        max_digits=12,
        default=Decimal("0.00"),
        help_text=_(u"Default product weight when no weight attribute is defined.")
    )

    class Meta:
        verbose_name = _("weight-based shipping method")
        verbose_name_plural = _("weight-based shipping methods")

    def calculate(self, cart):
        weight = cart.weight()
        charge = self.charge_for_weight(weight)

    def charge_for_weight(self, weight):
        weight = Decimal(weight)
        if not self.bands.exists():
            return Decimal("0.00")

        top_band = self.top_band
        if weight < top_band.upper_limit:
            band = self.get_band_for_weight(weight)
            return band.charge
        else:
            return top_band.charge

    @property
    def top_band(self):
        try:
            return self.bands.order_by('-upper_limit')[0]
        except IndexError:
            return None


    def get_band_for_weight(self, weight):
        try:
            return self.bands.filter(upper_limit__gte=weight).order_by('upper_limit')[0]
        except IndexError:
            return None

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
