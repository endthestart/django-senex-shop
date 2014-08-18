import calendar
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DeleteView, FormView, TemplateView, DetailView, UpdateView

from .exceptions import UnableToPlaceOrder, PaymentError
from .forms import GatewayForm, ShippingAddressForm, UserAddressForm
from .models import Order, OrderNumberGenerator, UserPaymentDetails, StripeCharge
from .mixins import OrderPlacementMixin
from .session import CheckoutSessionMixin
from ..contact.models import UserAddress

import stripe


class GatewayView(CheckoutSessionMixin, FormView):
    template_name = 'senex_shop/checkout/gateway.html'
    form_class = GatewayForm
    success_url = reverse_lazy('checkout_shipping_address')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.get_success_response()
        return super(GatewayView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GatewayView, self).get_form_kwargs()
        email = self.checkout_session.get_guest_email()
        if email:
            kwargs['initial'] = {
                'username': email,
            }
        return kwargs

    def form_valid(self, form):
        if form.is_guest_checkout() or form.is_new_account_checkout():
            email = form.cleaned_data['username']
            self.checkout_session.set_guest_email(email)

            if form.is_new_account_checkout():
                messages.info(
                    self.request,
                    _("Create your account and then you will be redirected back to the checkout process.")
                )
                self.success_url = "{0}?next={1}&email={2}".format(
                    reverse('register'),
                    urlquote(reverse('checkout_shipping_address')),
                    urlquote(email)
                )
        else:
            user = form.get_user()
            login(self.request, user)

        return self.get_success_response()

    def get_success_response(self):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.success_url


class ShippingAddressView(CheckoutSessionMixin, FormView):
    """
    Determine the shipping for the order.
    """
    template_name = 'senex_shop/checkout/shipping_address.html'
    form_class = ShippingAddressForm

    def get(self, request, *args, **kwargs):
        # Check if the user has items in the cart
        if request.cart.is_empty:
            messages.error(request, _("You need to add some items to your cart to checkout."))
            return HttpResponseRedirect(reverse('cart'))

        # Check that guests have entered an email address
        if not request.user.is_authenticated() and not self.checkout_session.get_guest_email():
            messages.error(request, _("Please sign in or enter your email address."))
            return HttpResponseRedirect(reverse('checkout_start'))

        #TODO: Enable shipping status on carts
        # Ensure that the shipping address is needed
        #if not request.cart.is_shipping_required():
        #    messages.info(request, _("Your cart does not require a shipping address to be submitted."))
        #    return HttpResponseRedirect(self.get_success_url())

        return super(ShippingAddressView, self).get(request, *args, **kwargs)

    def get_initial(self):
        return self.checkout_session.new_shipping_address_fields()

    def get_context_data(self, **kwargs):
        kwargs = super(ShippingAddressView, self).get_context_data(**kwargs)
        kwargs['cart'] = self.request.cart
        if self.request.user.is_authenticated():
            kwargs['addresses'] = self.get_available_addresses()
        return kwargs

    def get_available_addresses(self):
        return UserAddress.objects.filter(user=self.request.user).order_by('-is_default_shipping')

    def post(self, request, *args, **kwargs):
        # Check is shipping address was selected directly
        if self.request.user.is_authenticated() and 'address_id' in self.request.POST:
            address = UserAddress.objects.get(pk=self.request.POST['address_id'], user=self.request.user)
            action = self.request.POST.get('action', None)
            if action == 'ship_to':
                # User has selected a previous address to ship to
                self.checkout_session.ship_to_user_address(address)
                return HttpResponseRedirect(self.get_success_url())
            elif action == 'delete':
                address.delete()
                messages.info(self.request, _("Address deleted from your address book"))
                return HttpResponseRedirect(reverse('checkout_shipping_method'))
            else:
                return HttpResponseBadRequest()
        else:
            return super(ShippingAddressView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # Store the address details in the sessions and redirect to the next step.
        address_fields = dict(
            (k, v) for (k, v) in form.instance.__dict__.items()
            if not k.startswith('_')
        )
        self.checkout_session.ship_to_new_address(address_fields)
        return super(ShippingAddressView, self).form_valid(form)

    def get_success_url(self):
        return reverse('checkout_shipping_method')


class UserAddressUpdateView(CheckoutSessionMixin, UpdateView):
    """
    Update a UserAddress
    """
    template_name = 'senex_shop/checkout/user_address_form.html'
    form_class = UserAddressForm

    def get_queryset(self):
        return self.request.user.addresses.all()

    def get_form_kwargs(self):
        kwargs = super(UserAddressUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.info(self.request, _("Address saved."))
        return reverse('checkout_shipping_address')


class UserAddressDeleteView(CheckoutSessionMixin, DeleteView):
    """
    Delete an address
    """
    template_name = 'senex_shop/checkout/user_address_delete.html'

    def get_queryset(self):
        return self.request.user.addresses.all()

    def get_success_url(self):
        messages.info(self.request, _("Address deleted."))
        return reverse('checkout_shipping_address')


class ShippingMethodView(CheckoutSessionMixin, TemplateView):
    template_name = 'senex_shop/checkout/shipping_methods.html'

    def get(self, request, *args, **kwargs):
        if request.cart.is_empty:
            messages.error(request, _("You need to add some items to your cart to checkout."))
            return HttpResponseRedirect(reverse('cart'))

        if not request.cart.is_shipping_required():
            self.checkout_session.use_shipping_method('__free__')
            return self.get_success_response()

        if not self.checkout_session.is_shipping_address_set():
            messages.error(request, _("Please choose a shipping address."))
            return HttpResponseRedirect(reverse('checkout_shipping_address'))

        self._methods = self.get_available_shipping_methods()
        if len(self._methods) == 0:
            messages.warning(request, _("Shipping is unavailable for your chosen address - please choose another."))
            return HttpResponseRedirect(reverse('checkout_shipping_address'))
        elif len(self._methods) == 1:
            #self.checkout_session.use_shipping_method(self._methods[0].code)
            #defaulting to free shipping
            self.checkout_session.use_free_shipping()
            return self.get_success_response()

        return super(ShippingMethodView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(ShippingMethodView, self).get_context_data(**kwargs)
        kwargs['methods'] = self._methods
        return kwargs

    def get_available_shipping_methods(self):
        from senex_shop.shipping import methods
        #return Repository().get_shipping_methods(
        #    user=self.request.user,
        #    cart=self.request.cart,
        #    shipping_address=self.get_shipping_address(self.request.cart),
        #    request=self.request
        #)
        return (methods.Free(),)

    def post(self, request, *args, **kwargs):
        method_code = request.POST.get('method_code', None)
        is_valid = False
        for method in self.get_available_shipping_methods():
            if method.code == method.code:
                is_valid = True
        if not is_valid:
            messages.error(request, _("Your submitted shipping method is not permitted."))
            return HttpResponseRedirect(reverse('checkout_shipping_method'))

        self.checkout_session.use_shipping_method(method_code)
        return self.get_success_response()

    def get_success_response(self):
        return HttpResponseRedirect(reverse('checkout_payment_method'))


class PaymentMethodView(CheckoutSessionMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        # check that the user's cart is not empty
        if request.cart.is_empty:
            messages.error(request, _("You need to add some items to your cart to checkout"))
            return HttpResponseRedirect(reverse('cart'))

        shipping_required = request.cart.is_shipping_required()

        if shipping_required and not self.checkout_session.is_shipping_address_set():
            messages.error(request, _("Please choose a shipping address."))
            return HttpResponseRedirect(reverse('checkout_shipping_address'))

        if shipping_required and not self.checkout_session.is_shipping_method_set(self.request.cart):
            messages.error(request, _("Please choose a shipping method."))
            return HttpResponseRedirect(reverse('check_shipping_method'))

        return self.get_success_response()

    def get_success_response(self):
        return HttpResponseRedirect(reverse('checkout_payment_details'))


class PaymentDetailsView(OrderPlacementMixin, TemplateView):
    """
    Things to do for a successful checkout:
    1. Build the submission. Cart, shipping_address, shipping_method, total, and user.
    2. Build checkout form,
    """
    template_name = 'senex_shop/checkout/payment_details.html'
    template_name_preview = 'senex_shop/checkout/preview.html'
    preview = False
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    def get(self, request, *args, **kwargs):
        error_response = self.get_error_response()
        if error_response:
            return error_response
        return super(PaymentDetailsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        error_response = self.get_error_response()
        if error_response:
            return error_response

        if self.preview:
            if request.POST.get('action', '') == 'place_order':
                submission = self.build_submission()
                return self.submit(**submission)
            return self.render_preview(request)

        return self.get(request, *args, **kwargs)

    def get_error_response(self):
        if self.request.cart.is_empty:
            messages.error(
                self.request,
                _("You need to add some items to your cart to checkout.")
            )
            return HttpResponseRedirect(reverse('cart'))

        if self.request.cart.is_shipping_required():
            shipping_address = self.get_shipping_address(self.request.cart)
            if not shipping_address:
                messages.error(
                    self.request,
                    _("Please choose a shipping address. 4")
                )
                return HttpResponseRedirect(reverse('checkout_shipping_address'))

    def build_submission(self, **kwargs):
        shipping_address = self.get_shipping_address(self.request.cart)
        shipping_method = None
        submission = {
            'user': self.request.user,
            'cart': self.request.cart,
            'shipping_address': shipping_address,
            'shipping_method': shipping_method,
            'order_total': self.request.cart.total_price,
            'stripe_token': self.request.POST.get('stripeToken', None),
            'order_kwargs': {},
            'payment_kwargs': {},
        }
        if not submission['user'].is_authenticated():
            email = self.checkout_session.get_guest_email()
            submission['order_kwargs']['guest_email'] = email
        return submission

    def get_template_names(self):
        return [self.template_name_preview] if self.preview else [self.template_name]

    def render_preview(self, request, **kwargs):
        ctx = self.get_context_data()
        ctx.update(kwargs)
        return self.render_to_response(ctx)

    def submit(self, user, cart, shipping_address, shipping_method, order_total, stripe_token, payment_kwargs=None,
               order_kwargs=None):
        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}

        order_number = self.generate_order_number(cart)
        self.checkout_session.set_order_number(order_number)
        self.freeze_cart(cart)
        self.checkout_session.set_submitted_cart(cart)

        error_msg = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")

        try:
            charge = self.handle_payment(order_number, order_total, user, **payment_kwargs)
        except PaymentError, e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development.
            # logger.error(
            #    "Order #%s: unhandled exception while taking payment (%s)",
            #    order_number, e, exc_info=True)
            self.restore_frozen_cart(cart)
            self.preview = False
            messages.error(self.request, _("There was an error processing your payment. Please try again."))
            return self.render_to_response(self.get_context_data(error=unicode(e)))
        try:
            stripe_charge = StripeCharge()
            stripe_charge.from_charge(charge)
            stripe_charge.save()
            return self.handle_order_placement(order_number, user, cart, shipping_address, shipping_method, order_total, stripe_charge, **order_kwargs)
        except UnableToPlaceOrder, e:
            # logger.error(
            #    "Order #%s: unhandled exception while taking payment (%s)",
            #    order_number, e, exc_info=True)
            self.restore_frozen_cart(cart)
            self.preview = False
            return self.render_to_response(self.get_context_data(error=unicode(e)))

    def generate_order_number(self, cart):
        return OrderNumberGenerator().order_number(cart)

    def freeze_cart(self, cart):
        cart.freeze()

    def restore_frozen_cart(self, cart):
        cart.thaw()

    def handle_payment(self, order_number, total, user, **kwargs):
        """
        :param order_number:
        :param total:
        :param kwargs:
        :return:
        """
        token = self.request.POST.get('stripeToken', None)
        if not token:
            return HttpResponseRedirect(reverse('checkout_payment_details'))
        # email = self.request.POST.get('stripeEmail', None)
        # TODO: Add a get_email method that does this logic
        stripe.api_key = self.stripe_secret_key

        if user.is_authenticated():
            full_name = "{} {}".format(user.first_name, user.last_name)
            try:
                user_payment_details = UserPaymentDetails.objects.get(user=user)
            except UserPaymentDetails.DoesNotExist:
                user_payment_details = None

            if user_payment_details:
                try:
                    customer = stripe.Customer.retrieve(user_payment_details.stripe_id)
                except stripe.InvalidRequestError as e:
                    customer = stripe.Customer.create(card=token, description=full_name, email=user.email)
                    user_payment_details.stripe_id = customer.stripe_id
                    user_payment_details.save()
            else:
                customer = stripe.Customer.create(card=token, description=full_name, email=user.email)
                user_payment_details = UserPaymentDetails(user=user, stripe_id=customer.id)
                user_payment_details.save()

            try:
                charge = stripe.Charge.create(
                    amount=int(self.request.cart.total_less_discount * 100),
                    currency="usd",
                    customer=customer.id
                )
            except (stripe.CardError, stripe.InvalidRequestError) as e:
                messages.error(e)
                self.restore_frozen_cart(self.request.cart)
                self.preview = False
                return self.render_to_response(self.get_context_data(error=e.message))
        else:
            email = self.checkout_session.get_guest_email()
            try:
                charge = stripe.Charge.create(
                    amount=int(self.request.cart.total_less_discount * 100),
                    currency="usd",
                    card=token,
                    description=email
                )
            except (stripe.CardError, stripe.InvalidRequestError) as e:
                messages.error(e)
                self.restore_frozen_cart(self.request.cart)
                self.preview = False
                return self.render_to_response(self.get_context_data(error=e.message))
        return charge

    def get_context_data(self, **kwargs):
        ctx = self.build_submission(**kwargs)
        ctx['STRIPE_PUBLIC_KEY'] = self.stripe_public_key
        ctx['months'] = self.get_month_list()
        ctx['years'] = self.get_year_list()
        ctx.update(kwargs)
        ctx.update(ctx['order_kwargs'])
        return ctx

    def get_month_list(self):
        months = []
        for i in range(1, 13):
            months.append(
                {'value': str(i).zfill(2), 'display': "{} - {}".format(str(i).zfill(2), calendar.month_name[i]), })
        return months

    def get_year_list(self):
        years = []
        for i in range(0, 10):
            years.append(date.today().year + i)
        return years


class ThankYouView(DetailView):
    template_name = 'senex_shop/checkout/thank_you.html'
    context_object_name = 'order'

    def get_object(self):
        order = None
        if not order:
            if 'checkout_order_id' in self.request.session:
                order = Order.objects.get(pk=self.request.session['checkout_order_id'])
            elif self.request.GET.get('order_id', '') != '':
                # TODO: Make this accessible only by admins
                order = Order.objects.get(number=self.request.GET.get('order_id'))
            else:
                raise Http404(_("No order found"))

        return order
