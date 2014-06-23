from django.contrib import admin
from .models import CustomProduct


class CustomProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('option_group',)


admin.site.register(CustomProduct, CustomProductAdmin)
