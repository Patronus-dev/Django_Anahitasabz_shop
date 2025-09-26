from django.contrib import admin
from .models import Coupon, Shipping


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'active', 'datetime_created', 'datetime_expired')
    list_filter = ('active', 'discount_type')
    search_fields = ('code',)


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('shipping_method', 'cost', 'active')
    list_editable = ('cost', 'active')
    search_fields = ('shipping_method',)
    list_filter = ('active',)
