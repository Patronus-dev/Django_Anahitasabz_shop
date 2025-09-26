from django.urls import path
from .views import ProductListView, ProductDetailView, product_search_view

app_name = 'products'

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path('search/', product_search_view, name='user_search'),
]
