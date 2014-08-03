from django.db import models
from django.utils.translation import ugettext_lazy as _

from senex_shop.models import Product


class Discount(models.Model):
    ABSOLUTE, PERCENTAGE = (_(u"Absolute"), _(u"Percentage"))
    TYPE_CHOICES = (
        (ABSOLUTE, _(u"Absolute - an absolute dollar amount")),
        (PERCENTAGE, _(u"Percentage - a percentage of the total")),
    )
    name = models.CharField(
        _("name"),
        max_length=255,
        help_text=_("The name of the discount.")
    )
    code = models.CharField(
        _("code"),
        max_length=30,
        help_text=_("The code to use the discount."),
    )
    active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_("If the discount is active or not.")
    )
    type = models.CharField(
        _("type"),
        max_length=128,
        default=ABSOLUTE,
        choices=TYPE_CHOICES,
        help_text=_("The type of discount."),
    )
    value = models.DecimalField(
        _("value"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The amount of the discount."),
    )
    products = models.ManyToManyField(
        Product,
        verbose_name=_("products"),
        related_name="discounts",
    )

    def get_discount(self, cart):
        return 10

    def __unicode__(self):
        return self.name
