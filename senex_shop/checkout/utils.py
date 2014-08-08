import warnings


class CheckoutSessionData(object):
    SESSION_KEY = 'checkout_data'

    def __init__(self, request):
        self.request = request
        if self.SESSION_KEY not in self.request.session:
            self.request.session[self.SESSION_KEY] = {}

    def _check_namespace(self, namespace):
        if namespace not in self.request.session[self.SESSION_KEY]:
            self.request.session[self.SESSION_KEY][namespace] = {}

    def _get(self, namespace, key, default=None):
        """
        Return session value or None
        """
        self._check_namespace(namespace)
        if key in self.request.session[self.SESSION_KEY][namespace]:
            return self.request.session[self.SESSION_KEY][namespace][key]
        return default

    def _set(self, namespace, key, value):
        """
        Set session value
        """
        self._check_namespace(namespace)
        self.request.session[self.SESSION_KEY][namespace][key] = value
        self.request.session.modified = True

    def _unset(self, namespace, key):
        """
        Unset session value
        """
        self._check_namespace(namespace)
        if key in self.request.session[self.SESSION_KEY][namespace]:
            del self.request.session[self.SESSION_KEY][namespace][key]
            self.request.session.modified = True

    def _flush_namespace(self, namespace):
        self.request.session[self.SESSION_KEY][namespace] = {}
        self.request.session.modified = True

    def flush(self):
        """
        Delete session key
        """
        self.request.session[self.SESSION_KEY] = {}

    # Guest Checkout
    def set_guest_email(self, email):
        self._set('guest', 'email', email)

    def get_guest_email(self):
        return self._get('guest', 'email')

    # Shipping Address
    # Options:
    # 1. No shipping required
    # 2. Ship to new address (entered in form)
    # 3. Ship to an addressbook address (address chosen from list)

    def reset_shipping_data(self):
        self._flush_namespace('shipping')

    def ship_to_user_address(self, address):
        """
        Set existing shipping address id to session and unset address fields from session.
        """
        self.reset_shipping_data()
        self._set('shipping', 'user_address_id', address.id)

    def ship_to_new_address(self, address_fields):
        #TODO: Should this be unsetting 'user_address_id'???
        """
        Set new shipping address details to session and unset shipping address id.
        """
        self._unset('shipping', 'new_address_fields')
        self._set('shipping', 'new_address_fields', address_fields)

    def new_shipping_address_fields(self):
        """
        Get shipping address fields from session.
        """
        return self._get('shipping', 'new_address_fields')

    def shipping_user_address_id(self):
        """
        Get user address id from session.
        """
        return self._get('shipping', 'user_address_id')

    user_address_id = shipping_user_address_id

    def is_shipping_address_set(self):
        """
        Test whether a shipping address has been stored in the session.
        """
        new_fields = self.new_shipping_address_fields()
        has_new_address = new_fields is not None
        has_old_address = self.user_address_id() > 0
        return has_new_address or has_old_address

    # Shipping method

    def use_free_shipping(self):
        self._set('shipping', 'method_code', '__free__')

    def use_shipping_method(self, code):
        self._set('shipping', 'method_code', code)

    def shipping_method_code(self, cart):
        return self._get('shipping', 'method_code')

    def is_shipping_method_set(self, cart):
        return self.shipping_method_code(cart) is not None

    # Billing address fields
    def bill_to_new_address(self, address_fields):
        self._flush_namespace('billing')
        self._set('billing', 'new_address_fields', address_fields)

    def bill_to_user_address(self, address):
        self._flush_namespace('billing')
        self._set('billing', 'user_address_id', address.id)

    def bill_to_shipping_address(self):
        self._flush_namespace('billing')
        self._set('billing', 'billing_address_same_as_shipping, True')

    def is_billing_address_same_as_shipping(self):
        return self._get('billing', 'billing_address_same_as_shipping', False)

    def billing_user_address_id(self):
        return self._get('billing', 'user_address_id')

    def new_billing_address_fields(self):
        return self._get('billing', 'new_address_fields')

    # Payment methods
    def pay_by(self, method):
        self._set('payment', 'method', method)

    def payment_method(self):
        return self._get('payment', 'method')

    # Submission methods
    def set_order_number(self, order_number):
        self._set('submission', 'order_number', order_number)

    def get_order_number(self):
        return self._get('submission', 'order_number')

    def set_submitted_cart(self, cart):
        self._set('submission', 'cart_id', cart.id)

    def get_submitted_cart_id(self):
        return self._get('submission', 'cart_id')


