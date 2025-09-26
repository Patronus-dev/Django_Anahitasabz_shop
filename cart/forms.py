from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Coupon


class AddToCartProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        coerce=int,
        label=_('Quantity'),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)

        if product and product.quantity > 0:
            self.fields["quantity"].choices = [
                (i, str(i)) for i in range(1, product.quantity + 1)
            ]
        else:
            self.fields["quantity"].choices = []


class CouponForm(forms.Form):
    code = forms.CharField(
        max_length=50,
        label=_("Coupon Code"),
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Enter your coupon code")
        })
    )


class CouponAdminForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
        widgets = {
            "datetime_expired": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control"
                },
                format="%Y-%m-%dT%H:%M"
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.datetime_expired:
            self.initial["datetime_expired"] = self.instance.datetime_expired.strftime("%Y-%m-%dT%H:%M")
