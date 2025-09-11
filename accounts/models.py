from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = models.CharField(max_length=11, unique=True, null=False, blank=False, validators=[
        RegexValidator(regex=r"^09\d{9}$")], verbose_name=_("Phone Number"), help_text=_("09 "))
    name = models.CharField(default="", max_length=100, null=False, blank=False,
                            verbose_name=_("Name"), help_text=_("Enter your name."))
    lastname = models.CharField(default="", max_length=100, null=False, blank=False,
                                verbose_name=_("Lastname"), help_text=_("Enter your lastname."))
    province = models.CharField(default="", max_length=100, verbose_name=_("province"))
    city = models.CharField(default="", max_length=100, verbose_name=_("city"))
    address = models.TextField(default="", verbose_name=_("address"))
    postal_code = models.CharField(default="", max_length=10, verbose_name=_("postal_code"))

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "lastname", "province", "city", "address", "postal_code"]

    def __str__(self):
        return f"{self.username} - {self.name} {self.lastname}"
