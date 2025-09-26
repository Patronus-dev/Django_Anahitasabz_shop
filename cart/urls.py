from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path("", cart_detail_view, name="cart_detail"),
    path("add/<int:product_id>/", add_to_cart_view, name="cart_add"),
    path("remove/<int:product_id>/", remove_from_cart, name="cart_remove"),
    path("clear/", cart_clear, name="cart_clear"),
    path("apply-coupon/", apply_coupon, name="apply_coupon"),
    path('set-shipping/', set_shipping, name='set_shipping'),
]
