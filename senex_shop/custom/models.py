from django.db import models
from senex_shop.models import Product, OptionGroup
from django.utils.translation import ugettext_lazy as _

from senex_shop import utils

STORE_PRODUCT = True


def get_product_types():
    return ('CustomProduct',)


class CustomProduct(models.Model):
    product = models.OneToOneField(
        Product,
        verbose_name=_('Product'),
        primary_key=True,
    )
    option_group = models.ManyToManyField(
        OptionGroup,
        verbose_name=_('option group'),
        blank=True,
    )

    @property
    def unit_price(self):
        return self.product.unit_price

    def add_template_context(self, context, selected_options, **kwargs):
        """
        Add context for the product template.
        Return the updated context.
        """

        #options = utils.serialize_options(self, selected_options)
        options = self.option_group.all()
        if not 'options' in context:
            context['options'] = options
        else:
            curr = list(context['options'])
            curr.extend(list(options))
            context['options'] = curr

        return context

    def _get_subtype(self):
        return 'CustomProduct'

    def __unicode__(self):
        return u"CustomProduct: {0}".format(self.product.name)

    def get_valid_options(self):
        """
        Returns all of the valid options
        """
        return utils.get_all_options(self, ids_only=True)

    def save(self, **kwargs):
        if hasattr(self.product, '_sub_types'):
            del self.product._sub_types
        super(CustomProduct, self).save(**kwargs)

    class Meta:
        verbose_name = _("Custom Product")
        verbose_name_plural = _("Custom Products")
