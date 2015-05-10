__version__ = '0.2.3'

def active_product_types():
    """Get a list of activated product modules, in the form of
    [(module, config module name),...]
    """
    from django.db import models

    gateways = []
    for app in models.get_apps():
        if hasattr(app, 'STORE_PRODUCT'):
            parts = app.__name__.split('.')[:-1]
            module = ".".join(parts)
            if hasattr(app, 'get_product_types'):
                subtypes = app.get_product_types()
                for subtype in subtypes:
                    gateways.append((module, subtype))
            else:
                gateways.append((module, parts[-1].capitalize() + 'Product'))

    return gateways
