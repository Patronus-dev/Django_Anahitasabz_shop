from django.contrib import admin
from .models import SiteContactInfo


@admin.register(SiteContactInfo)
class SiteContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # فقط اجازه اضافه کردن وقتی هیچ رکوردی وجود نداره
        if SiteContactInfo.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # حذف آزاد باشه
        return True
