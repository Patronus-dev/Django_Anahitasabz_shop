from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path("checkout/", checkout_view, name="checkout"),
]
