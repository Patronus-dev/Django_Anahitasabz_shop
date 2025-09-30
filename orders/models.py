from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False, verbose_name=_('Payment status'))

    order_notes = models.TextField(max_length=500, blank=True, verbose_name=_('Order notes'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date edited'))

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        verbose_name = _("Orders")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items',
                                verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    price = models.PositiveIntegerField(verbose_name=_("Price"))

    def __str__(self):
        return f"OrderItem {self.id}: {self.product} x {self.quantity} (price: {self.price})"

    class Meta:
        verbose_name = _("Order items")
        verbose_name_plural = _("Order Items")
