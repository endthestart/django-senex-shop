from django import forms

from senex_shop.discounts.models import Discount


class DiscountForm(forms.Form):
    discount_code = forms.CharField(label="Discount Code", max_length=30)

    def clean_discount_code(self):
        cleaned_code = self.cleaned_data['discount_code']
        try:
            Discount.objects.get(code=cleaned_code)
        except Discount.DoesNotExist:
            raise forms.ValidationError("Unable to match this discount code.")
        return cleaned_code
