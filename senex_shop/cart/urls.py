from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'senex_shop.cart.views.cart', name='cart'),
                       url(r'^add/$', 'senex_shop.cart.views.add', name='cart_add'),
                       url(r'^remove/$', 'senex_shop.cart.views.remove', name='cart_remove'),
                       url(r'^quantity/$', 'senex_shop.cart.views.set_quantity', name='cart_quantity'),
)
