from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..cart.models import Cart
from ..contact.models import BillingAddress, ShippingAddress

from django.conf import settings


USER_MODULE_PATH = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class StripeCharge(models.Model):
    charge_id = models.CharField(max_length=32)
    card_brand = models.CharField(max_length=32)
    last4 = models.CharField(max_length=4)

    def from_charge(self, charge):
        self.charge_id = charge.id
        self.card_brand = charge.card.brand
        self.last4 = charge.card.last4

    def __unicode__(self):
        return u"Stripe Charge: {}".format(self.charge_id)

    class Meta:
        verbose_name = _("stripe charge")
        verbose_name_plural = _("stripe charges")
        ordering = ('charge_id',)


class Order(models.Model):
    number = models.CharField(
        _("order number"),
        max_length=128,
        db_index=True,
    )
    cart = models.ForeignKey(
        Cart,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        USER_MODULE_PATH,
        blank=True,
        null=True,
        verbose_name=_("user"),
    )
    billing_address = models.ForeignKey(
        BillingAddress,
        null=True,
        blank=True,
        verbose_name=_("billing address"),
    )
    total_incl_tax = models.DecimalField(
        _("order total (inc. tax)"),
        decimal_places=2,
        max_digits=12,
    )
    total_excl_tax = models.DecimalField(
        _("order total (excl tax)"),
        decimal_places=2,
        max_digits=12,
    )
    shipping_incl_tax = models.DecimalField(
        _("shipping charge (inc. tax)"),
        decimal_places=2,
        max_digits=12,
    )
    shipping_excl_tax = models.DecimalField(
        _("shipping charge (excl. tax)"),
        decimal_places=2,
        max_digits=12,
    )
    shipping_address = models.ForeignKey(
        ShippingAddress,
        null=True,
        blank=True,
        verbose_name=_("shipping address"),
    )
    shipping_method = models.CharField(
        _("shipping method"),
        max_length=128,
        null=True,
        blank=True,
    )
    shipping_code = models.CharField(
        blank=True,
        max_length=128,
        default='',
    )
    status = models.CharField(
        _("status"),
        max_length=100,
        null=True,
        blank=True,
    )
    guest_email = models.EmailField(
        _("guest email address"),
        null=True,
        blank=True,
    )
    date_ordered = models.DateField(
        auto_now_add=True,
        db_index=True,
    )
    charge = models.ForeignKey(
        StripeCharge,
        null=True,
        blank=True,
        verbose_name=_("charge"),
    )

    @property
    def is_anonymous(self):
        return self.user is None

    @property
    def email(self):
        if not self.user:
            return self.guest_email
        return self.user.email

    def __unicode__(self):
        return u"Order - {} - {}".format(self.user.get_full_name(), self.number)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ('user',)


class OrderNumberGenerator(object):
    def order_number(self, cart):
        return 100000 + cart.id


class OrderCreator(object):
    """
    Places the order by creating the various models
    """

    def place_order(self, cart, total, user=None, shipping_method=None, shipping_address=None,
                    billing_address=None, order_number=None, charge=None, status=None, **kwargs):
        if cart.is_empty:
            raise ValueError(_("Empty carts cannot be submitted"))
        if not order_number:
            generator = OrderNumberGenerator()
            generator.order_number(cart)

        try:
            Order.objects.get(number=order_number)
        except Order.DoesNotExist:
            pass
        else:
            raise ValueError(_("There is already an order with number {}".format(order_number)))

        order = self.create_order_model(user, cart, shipping_address, shipping_method, billing_address, total,
                                        order_number, charge, status, **kwargs)

        #TODO: Maybe convert a cart into actual order line items

        return order

    def create_order_model(self, user, cart, shipping_address, shipping_method, billing_address, total, order_number,
                           charge, status, **extra_order_fields):
        order_data = {
            'cart_id': cart.id,
            'number': order_number,
            'charge': charge,
            'total_incl_tax': total,
            'total_excl_tax': total,
            'shipping_incl_tax': 0,
            'shipping_excl_tax': 0,
            'shipping_method': shipping_method,
            'shipping_code': 0,
            'status': 0,
        }
        if shipping_address:
            order_data['shipping_address'] = shipping_address
        if billing_address:
            order_data['billing_address'] = billing_address
        if user and user.is_authenticated():
            order_data['user'] = user
        if extra_order_fields:
            order_data.update(extra_order_fields)
        order = Order(**order_data)
        order.save()
        return order


class PaymentType(models.Model):
    name = models.CharField(
        _("payment name"),
        max_length=128,
        null=False,
        blank=False,
    )
    code = models.SlugField(
        max_length=128,
        null=False,
        blank=False,
    )


class PaymentDetails(models.Model):
    """
    A place to store details about the payment.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
    )
    payment_type = models.ForeignKey(
        PaymentType,
        null=False,
        blank=False,
    )
    amount = models.DecimalField(
        _("amount of transaction"),
        decimal_places=2,
        max_digits=12,
    )

    def charge(self):
        pass

    def refund(self):
        pass


class UserPaymentDetails(models.Model):
    """
    A place to store details about a contact's various payment methods
    """
    user = models.ForeignKey(
        USER_MODULE_PATH,
        blank=True,
        null=True,
        verbose_name=_("user"),
    )

    stripe_id = models.CharField(
        _("stripe id"),
        max_length=128,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u"Payment Details: {}".format(self.user.get_full_name())

    class Meta:
        verbose_name = _("User Payment Details")
        verbose_name_plural = _("User Payment Details")
        ordering = ('user',)