from .utils import CheckoutSessionData
from senex_shop.contact.models import ShippingAddress, UserAddress


class CheckoutSessionMixin(object):
    """
    Mixin to provide common functionality between checkout views.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Assign the checkout session manager so it's available in all checkout views.
        """
        self.checkout_session = CheckoutSessionData(request)
        return super(CheckoutSessionMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Assign common template variable to the context.
        """
        context = super(CheckoutSessionMixin, self).get_context_data(**kwargs)

        cart = self.request.cart
        shipping_address = self.get_shipping_address(cart)
        #shipping_method = self.get_shipping_method(cart, shipping_address)

        context['shipping_address'] = shipping_address
        #context['shipping_method'] = shipping_method

        #if cart and shipping_method:
        #    context['order_total'] = self.get_order_totals(cart, shipping_method)

        return context

    def get_shipping_address(self, cart):
        """
        Return the (unsaved) shipping address for this checkout session.
        """
        address_data = self.checkout_session.new_shipping_address_fields()
        if address_data:
            return ShippingAddress(**address_data)
        address_id = self.checkout_session.user_address_id()
        if address_id:
            try:
                address = UserAddress.objects.get(pk=address_id)
            except UserAddress.DoesNotExist:
                return None
            else:
                shipping_address = ShippingAddress()
                address.populate_alternative_model(shipping_address)
                return address

        #def get_shipping_method(self, cart, shipping_address=None, **kwargs):
        #    """
        #    Return the selected shipping method instance from this checkout session.
        #    """
        #    code = self.checkout_session.shipping_method_code(cart)
        #    methods = Repository().get_shipping_methods(
        #        user=self.request.user,
        #        cart=cart,
        #        shipping_address=shipping_address,
        #        request=self.request
        #    )
        #    methods = {}
        #    for method in methods:
        #        if method.code == code:
        #            return method

        #def get_order_totals(self, cart, shipping_method, **kwargs):
        #    """
        #    Returns the total for the order with and without tax (as a tuple).`
        #    """
        #    return OrderTotalCalculator(self.request).calculate(cart, shipping_method, **kwargs)
