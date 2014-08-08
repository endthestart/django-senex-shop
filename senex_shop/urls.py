from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'senex_shop.views.store_home', name='store_home'),
                       url(r'^emailcheck/$', 'senex_shop.views.email_check', name='email_check'),
                       url(r'^(?P<path>.+)/p/(?P<slug>[-\w]+)/$', 'senex_shop.views.product_detail', name='product_detail'),
                       url(r'^(?P<path>.+)/$', 'senex_shop.views.category', name='category'),
                       url(r'^emailcheck/$', 'senex_shop.views.email_check', name='email_check'),

)
