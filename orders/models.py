from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import jdatetime
from django.utils.timezone import localtime


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('shipped', _('Shipped')),
        ('completed', _('Completed')),
        ('canceled', _('Canceled')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    is_paid = models.BooleanField(default=False, verbose_name=_('Payment status'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))

    total_price = models.PositiveIntegerField(default=0, verbose_name=_('Total price'))
    shipping_method = models.ForeignKey(
        'cart.Shipping', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Shipping method')
    )
    coupon_code = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Coupon code'))
    coupon_value = models.PositiveIntegerField(default=0, verbose_name=_('Coupon Value'))  # مبلغ تخفیف
    coupon_display = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Coupon Display'))  # مثلا %10

    order_notes = models.TextField(max_length=500, blank=True, verbose_name=_('Order notes'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date edited'))

    def __str__(self):
        return f"Order {self.id} - {self.user}"

    @property
    def order_number(self):
        """شماره سفارش اختصاصی (شمسی)"""
        jalali_date = jdatetime.datetime.fromgregorian(datetime=localtime(self.datetime_created))
        return f"00{jalali_date.strftime('%Y%m%d')}{self.id}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Product')
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    price = models.PositiveIntegerField(verbose_name=_("Price"))  # ذخیره‌ی قیمت واحد محصول در لحظه خرید

    def __str__(self):
        return f"{self.product} x {self.quantity} (price: {self.price})"

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")
