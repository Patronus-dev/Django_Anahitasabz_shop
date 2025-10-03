from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path("create/", order_create_view, name="order_create"),
    path('order_detail/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
]
