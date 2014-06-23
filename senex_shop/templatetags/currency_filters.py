from decimal import Decimal, InvalidOperation

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()


@register.filter(name='currency')
def currency(value):
    """
    Format decimal value as currency.
    """
    try:
        value = round(Decimal(value), 2)
    except (TypeError, InvalidOperation):
        return u""

    return "${dollars}{cents}".format(dollars=intcomma(int(value)), cents=("%0.2f" % value)[-3:])
