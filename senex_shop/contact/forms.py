from django.conf import settings
from django import forms

from .models import UserAddress


class AbstractAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbstractAddressForm, self).__init__(*args, **kwargs)
        #field_names = (set(self.fields) &
        #               set(settings.OSCAR_REQUIRED_ADDRESS_FIELDS))
        #for field_name in field_names:
        #    self.fields[field_name].required = True


class UserAddressForm(AbstractAddressForm):
    class Meta:
        model = UserAddress
        exclude = ('user', 'num_orders', 'is_default_billing', 'is_default_shipping')

    def __init__(self, user, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        self.instance.user = user
