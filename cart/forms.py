from django import forms
from django.utils.translation import gettext_lazy as _


class AddToCartProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        coerce=int,
        label=_('Quantity')
    )

    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)

        if product:
            self.fields["quantity"].choices = [
                (i, str(i)) for i in range(1, product.quantity + 1)
            ]
        else:
            self.fields["quantity"].choices = []
