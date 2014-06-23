from django.contrib import admin
from .models import Category, Product, ProductImage, OptionGroup, Option


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('path', 'name_path')
    list_display = ('name', 'is_active', 'path')
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ProductImageInline,
    ]


class OptionInline(admin.TabularInline):
    model = Option


class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(Option)
admin.site.register(ProductImage)
