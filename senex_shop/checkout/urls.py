from django.conf.urls import patterns, url

from senex_shop.checkout.views import GatewayView, ShippingAddressView, ShippingMethodView, PaymentMethodView, \
    PaymentDetailsView, UserAddressUpdateView, UserAddressDeleteView, ThankYouView

urlpatterns = patterns('',
                       url(r'^$', GatewayView.as_view(), name='checkout_start'),
                       url(r'^shipping-address/$', ShippingAddressView.as_view(), name='checkout_shipping_address'),
                       url(r'^shipping-address/edit/(?P<pk>\d+)/$', UserAddressUpdateView.as_view(),
                           name='checkout_user_address_update'),
                       url(r'^shipping-address/delete/(?P<pk>\d+)/$', UserAddressDeleteView.as_view(),
                           name='checkout_user_address_delete'),
                       url(r'^shipping-method/$', ShippingMethodView.as_view(), name='checkout_shipping_method'),
                       url(r'^payment-method/$', PaymentMethodView.as_view(), name='checkout_payment_method'),
                       url(r'^payment-details/$', PaymentDetailsView.as_view(), name='checkout_payment_details'),
                       url(r'^preview/$', PaymentDetailsView.as_view(preview=True), name='checkout_preview'),
                       url(r'^thank-you/$', ThankYouView.as_view(), name='checkout_thank_you'),
)
