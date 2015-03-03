from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'email', 'date_ordered', )
    raw_id_fields = ('user', 'cart', 'billing_address', 'shipping_address', 'charge', )


admin.site.register(Order, OrderAdmin)
