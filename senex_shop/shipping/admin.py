from django.contrib import admin

from .models import OrderAndItemsCharges, WeightBand, WeightBased


class OrderChargesAdmin(admin.ModelAdmin):
    exclude = ('code',)
    list_display = ('name', 'description', 'price_per_order', 'price_per_item', 'free_shipping_threshold')


class WeightBandAdmin(admin.ModelAdmin):
    list_display = ('method', 'weight_from', 'weight_to', 'charge')


admin.site.register(OrderAndItemsCharges, OrderChargesAdmin)
admin.site.register(WeightBased)
admin.site.register(WeightBand, WeightBandAdmin)

