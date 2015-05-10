from datetime import date, datetime
from calendar import monthrange

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.dates import MONTHS
from django.utils.translation import ugettext_lazy as _

from senex_shop.contact.forms import AbstractAddressForm
from senex_shop.contact.models import ShippingAddress, UserAddress
from senex_shop.contact.utils import normalize_email

from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.forms import USStateSelect, USZipCodeField


class ShippingAddressForm(AbstractAddressForm):
    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ShippingAddress
        exclude = ('user', 'country')

    widgets = {
        'state': USStateSelect(),
    }


class UserAddressForm(AbstractAddressForm):
    class Meta:
        model = UserAddress
        exclude = ('user', 'is_default_billing', 'is_default_shipping')

    def __init__(self, user, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        self.instance.user = user


class GatewayForm(AuthenticationForm):
    username = forms.EmailField(label=_("My email address is:"))
    GUEST, NEW, EXISTING = 'anonymous', 'new', 'existing'
    CHOICES = (
        (NEW, _("No, I am a new customer.")),
        (GUEST, _("I want to checkout as a guest.")),
        (EXISTING, _("Yes, and my password is:")),
    )
    options = forms.ChoiceField(widget=forms.widgets.RadioSelect, choices=CHOICES, initial=GUEST)

    def clean_username(self):
        return normalize_email(self.cleaned_data['username'])

    def clean(self):
        if self.is_guest_checkout() or self.is_new_account_checkout():
            if 'password' in self.errors:
                del self.errors['password']
            if 'username' in self.cleaned_data:
                email = normalize_email(self.cleaned_data['username'])
                if get_user_model().objects.filter(email=email).exists():
                    msg = "A user with that email already exists"
                    self._errors["username"] = self.error_class([msg])
            return self.cleaned_data
        return super(GatewayForm, self).clean()

    def is_guest_checkout(self):
        return self.cleaned_data.get('options', None) == self.GUEST

    def is_new_account_checkout(self):
        return self.cleaned_data.get('options', None) == self.NEW


class CreditCardField(forms.IntegerField):
    def clean(self, value):
        """
        Check if the given cc number is valid and one of the card types we accept.
        """
        if value and (len(value) < 13 or len(value) > 16):
            raise forms.ValidationError("Please enter a valid credit card number.")
        return super(CreditCardField, self).clean(value)


class CCExpWidget(forms.MultiWidget):
    """
    Widget containing two select boxes for selecting the month and year.
    """

    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]

    def format_output(self, rendered_widgets):
        html = u"/".join(rendered_widgets)
        return u'<span stlye="white-space: nowrap;">{html}</span>'.format(html=html)


class CCExpField(forms.MultiValueField):
    EXP_MONTH = [(x, x) for x in xrange(1, 13)]
    EXP_YEAR = [(x, x) for x in xrange(date.today().year, date.today().year + 15)]

    default_error_messages = {
        'invalid_month': u"Enter a valid month.",
        'invalid_year': u"Enter a valid year.",
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.ChoiceField(
                choices=self.EXP_MONTH,
                error_messages={'invalid': errors['invalid_month']}
            ),
            forms.ChoiceField(
                choices=self.EXP_YEAR,
                error_messages={'invalid': errors['invalid_year']}
            ),
        )

        super(CCExpField, self).__init__(fields, *args, **kwargs)
        self.widget = CCExpField(widgets=[fields[0].widget, fields[1].widget])

    def clean(self, value):
        exp = super(CCExpField, self).clean(value)
        if date.toda() > exp:
            raise forms.ValidationError(
                "The expiration date you entered is in the pase."
            )
        return exp

    def compress(self, data_list):
        if data_list:
            if data_list[1] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_year']
                raise forms.ValidationError(error)
            if data_list[0] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_month']
                raise forms.ValidationError(error)
            year = int(data_list[1])
            month = int(data_list[0])
            day = monthrange(year, month)[1]

            return date(year, month, day)
        return None