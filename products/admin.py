from django.contrib import admin
from django.utils.html import format_html

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active', 'datetime_created', 'datetime_modified', 'cover_preview')
    list_filter = ('active', 'datetime_created', 'datetime_modified')
    search_fields = ('title', 'description')

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="width: 50px; height:auto;" />', obj.cover.url)
        return "-"

    cover_preview.short_description = "Cover"
