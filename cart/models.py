from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import django_jalali.db.models as jmodels

User = get_user_model()

class Coupon(models.Model):
    CODE_TYPE_CHOICES = [
        ('percent', _('Percentage')),
        ('fixed', _('Fixed Amount')),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name=_("Coupon Code"))
    discount_type = models.CharField(
        max_length=10, choices=CODE_TYPE_CHOICES, default='percent', verbose_name=_("Discount Type")
    )
    discount_value = models.PositiveIntegerField(verbose_name=_("Discount Value"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    datetime_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    datetime_expired = jmodels.jDateTimeField(null=True, blank=True, verbose_name=_("Expired At"))

    # لیست کاربران که این کوپن را استفاده کرده‌اند
    used_by = models.ManyToManyField(User, blank=True, related_name='used_coupons', verbose_name=_("Used By"))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")


class Shipping(models.Model):
    shipping_method = models.CharField(max_length=100, verbose_name=_("Shipping Method"))
    cost = models.PositiveIntegerField(default=0, verbose_name=_("Cost"))
    cost_on_delivery = models.BooleanField(default=False, verbose_name=_("Cost Paid by Receiver"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        if self.cost_on_delivery:
            return f"{self.shipping_method} - Payment on delivery"
        return f"{self.shipping_method} - {self.cost} Toman"

    class Meta:
        verbose_name = _("Shipping")
        verbose_name_plural = _("Shipping Methods")
