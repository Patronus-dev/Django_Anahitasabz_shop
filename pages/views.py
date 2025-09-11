from django.views.generic import *


class HomePageView(TemplateView):
    template_name = 'home.html'


class ContactUsView(TemplateView):
    template_name = 'pages/contact_us.html'
