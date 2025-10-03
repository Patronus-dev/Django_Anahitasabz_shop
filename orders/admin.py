from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali
import jdatetime
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price']
    extra = 1


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['user',
                    'order_number_display',
                    'datetime_created',
                    'total_price',
                    'coupon_code',
                    'coupon_display',
                    'is_paid'
                    ]
    list_filter = ['is_paid', 'datetime_created']
    search_fields = ['id', 'order_number_display', 'user__username']

    inlines = [OrderItemInline]

    def order_number_display(self, obj):
        """نمایش شماره سفارش اختصاصی"""
        return obj.order_number
    order_number_display.short_description = _("Order number")

    def jalali_datetime_created(self, obj):
        """نمایش تاریخ ایجاد به شمسی"""
        return datetime2jalali(obj.datetime_created).strftime('%Y/%m/%d - %H:%M')
    jalali_datetime_created.short_description = _("datetime_created")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'order', 'product', 'quantity', 'price', 'total_price']
    search_fields = ['order_number', 'product__name']
    readonly_fields = ['price', 'total_price', 'order_number']

    def order_number(self, obj):
        jalali_date = jdatetime.datetime.fromgregorian(datetime=localtime(obj.order.datetime_created))
        return f"00{jalali_date.strftime('%Y%m%d')}{obj.order.id}"
    order_number.short_description = _("Order number")

    def total_price(self, obj):
        return obj.price * obj.quantity
    total_price.short_description = _("total price")
