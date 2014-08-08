from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class CartManager(models.Manager):
    status_filter = 'Open'

    def get_for_request(self, request):
        session_cart = None
        if 'cart' in request.session:
            try:
                session_cart = self.get(pk=request.session['cart'], status=self.status_filter)
            except ObjectDoesNotExist:
                # TODO: This should be Cart.DoesNotExist but doesn't work
                session_cart = None

        if request.user.is_authenticated():
            cart = self.get_or_create(user=request.user, status=self.status_filter)[0]
            if session_cart:
                self.merge_carts(cart, session_cart)
                session_cart.delete()
                del request.session['cart']
        elif session_cart:
            cart = session_cart
        else:
            cart = self.create(user=None)
            request.session['cart'] = cart.pk
        return cart

    def merge_carts(self, master, slave):
        master.merge(slave)


class OpenCartManager(models.Manager):
    status_filter = "Open"

    def get_queryset(self):
        return super(OpenCartManager, self).get_queryset().filter(status=self.status_filter)

    def get_or_create(self, **kwargs):
        return self.get_queryset().get_or_create(status=self.status_filter, **kwargs)