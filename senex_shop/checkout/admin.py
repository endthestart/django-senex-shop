from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'email', 'date_ordered', )
    search_fields = ('number', )


admin.site.register(Order, OrderAdmin)
