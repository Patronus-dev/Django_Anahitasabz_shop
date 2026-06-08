from django.urls import path
from .views import *

app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),

]
