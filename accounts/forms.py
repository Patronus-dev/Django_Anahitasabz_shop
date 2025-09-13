from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', )


class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "lastname", "province", "city", "address", "postal_code"]


class PhoneLoginForm(forms.Form):
    phone = forms.CharField(max_length=11, label=_("Phone Number"), help_text=_("Enter your phone number."))


class VerifyOTPForm(forms.Form):
    code = forms.CharField(max_length=4, label=_("OTP code"))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["name", "lastname", "province", "city", "address", "postal_code"]