from django.contrib import admin
from .models import SiteContactInfo


@admin.register(SiteContactInfo)
class SiteContactInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'instagram_id', 'whatsapp_number', 'telegram_id')
    fieldsets = (
        (None, {
            'fields': ('name', 'phone_number')
        }),
        ('Social Media Links', {
            'fields': ('instagram_id', 'whatsapp_number', 'telegram_id')
        }),
    )

    # اگر میخوای فقط یک رکورد داشته باشه، میتونی اضافه کردن جدید رو محدود کنی
    def has_add_permission(self, request):
        return not SiteContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
