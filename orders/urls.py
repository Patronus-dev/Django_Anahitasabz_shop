from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path("checkout/", checkout_view, name="checkout"),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
]
