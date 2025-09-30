from django import forms
from accounts.models import CustomUser


class CheckoutUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'lastname', 'province', 'city', 'address', 'postal_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input form__input--2'}),
            'lastname': forms.TextInput(attrs={'class': 'form__input form__input--2'}),
            'province': forms.TextInput(attrs={'class': 'form__input form__input--2'}),
            'city': forms.TextInput(attrs={'class': 'form__input form__input--2'}),
            'address': forms.Textarea(attrs={'class': 'form__input form__input--2', 'rows': 2}),
            'postal_code': forms.TextInput(attrs={'class': 'form__input form__input--2'}),
        }
