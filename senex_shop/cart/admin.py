from django.contrib import admin

from .models import Cart, CartItem, CartItemDetails


class CartItem_Inline(admin.TabularInline):
    model = CartItem
    extra = 3
    raw_id_fields = ('product',)


class CartItemDetails_Inline(admin.StackedInline):
    model = CartItemDetails
    extra = 1


class CartOptions(admin.ModelAdmin):
    list_display = ('created', 'num_items', 'total_price')
    inlines = [CartItem_Inline]


class CartItemOptions(admin.ModelAdmin):
    inlines = [CartItemDetails_Inline]


admin.site.register(Cart, CartOptions)
admin.site.register(CartItem, CartItemOptions)
