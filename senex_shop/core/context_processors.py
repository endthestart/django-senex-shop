import logging

from senex_shop.core.models import Shop
logger = logging.getLogger("default")


def get_default_shop(request):
    try:
        shop = Shop.objects.get(pk=1)
    except Shop.DoesNotExist:
        logger.error("A shop must be configured for the site to function.")
        shop = None

    context = {'shop': shop}
    return context