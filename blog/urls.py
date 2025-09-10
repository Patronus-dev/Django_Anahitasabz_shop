from django.urls import path

from .views import *

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    # path('<int:pk>/like/', blog_like, name='blog_like'),
]
