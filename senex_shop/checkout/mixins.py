import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string

from .models import Cart, OrderCreator, StripeCharge
from .session import CheckoutSessionMixin
from ..contact.models import ShippingAddress, UserAddress, BillingAddress


class OrderPlacementMixin(CheckoutSessionMixin):
    def handle_order_placement(self, order_number, user, cart, shipping_address, shipping_method, total, charge, **kwargs):
        order = self.place_order(order_number, user, cart, shipping_address, shipping_method, total, charge, **kwargs)
        cart.submit()
        return self.handle_successful_order(order, charge)

    def place_order(self, order_number, user, cart, shipping_address, shipping_method, total, charge, billing_address=None,
                    **kwargs):
        shipping_address = self.create_shipping_address(user, shipping_address)
        billing_address = self.create_billing_address(billing_address, shipping_address, **kwargs)

        # TODO: Add charge as a field on Order model
        # TODO: Implement status for orders
        # if 'status' not in kwargs:
        #     status = self.get_initial_order_status(cart)
        # else
        #     status = kwargs.pop('status')

        order = OrderCreator().place_order(
            user=user,
            order_number=order_number,
            charge=charge,
            cart=cart,
            shipping_address=shipping_address,
            shipping_method=shipping_method,
            total=total,
            billing_address=billing_address,
            status=None,
            **kwargs
        )
        return order

    def handle_successful_order(self, order, charge):
        """
        Handle the status required after an order has been placed.
        """

        self.send_confirmation_message(order)

        # Flush all checkout session data
        self.checkout_session.flush()

        # Save the order id to the session for the thank-you page
        self.request.session['checkout_order_id'] = order.id

        response = HttpResponseRedirect(self.get_success_url())
        return response

    def get_success_url(self):
        return reverse('checkout_thank_you')

    def create_shipping_address(self, user, shipping_address):
        """
        Create and return the shipping address for the current order.

        Compared to the self.get_shipping_address(), ShippingAddress is actually saved
        and not editable.
        """
        shipping_address.save()
        if user.is_authenticated():
            self.update_address_book(user, shipping_address)
        return shipping_address

    def update_address_book(self, user, shipping_address):
        try:
            user_address = user.addresses.get(hash=shipping_address.generate_hash())
        except ObjectDoesNotExist:
            user_address = UserAddress(user=user)
            shipping_address.populate_alternative_model(user_address)
        user_address.save()

    def create_billing_address(self, billing_address=None, shipping_address=None, **kwargs):
        """
        Save the billing data
        """
        return None

    def get_initial_order_status(self):
        return None

    def get_submitted_cart(self):
        cart_id = self.checkout_session.get_submitted_cart_id()
        return Cart.objects.get(pk=cart_id)

    def restore_frozen_cart(self):
        try:
            frozen_cart = self.get_submitted_cart()
        except Cart.DoesNotExist:
            pass
        else:
            frozen_cart.thaw()
            #TODO: If there is another cart in the session, merge them

    def send_confirmation_message(self, order, **kwargs):
        from django.core.mail import EmailMultiAlternatives
        html_template = 'senex_shop/email/order_confirmation_body.html'
        text_template = 'senex_shop/email/order_confirmation_body.txt'
        subject_template = 'senex_shop/email/order_confirmation_subject.txt'
        context = {'order': order}
        email_text = render_to_string(text_template, context)
        email_html = render_to_string(html_template, context)
        email_subject = render_to_string(subject_template, context)
        email = EmailMultiAlternatives(email_subject, email_text, 'info@senexcycles.com', [order.user.email])
        email.attach_alternative(email_html, "text/html")
        email.send()


