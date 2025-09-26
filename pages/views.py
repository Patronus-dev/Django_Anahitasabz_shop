from django.views.generic import *

from .models import SiteContactInfo


class HomePageView(TemplateView):
    template_name = 'home.html'


class ContactUsView(TemplateView):
    template_name = 'pages/contact_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # فقط اولین رکورد موجود را می‌گیریم
        admin_info = SiteContactInfo.objects.first()
        context['admin_info'] = admin_info
        return context
