from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "datetime_created", "datetime_modified")
    list_filter = ("status", "datetime_created", "datetime_modified")
    search_fields = ("title", "author", "source", "text")
    ordering = ("-datetime_created",)

    # فقط خوندنی نمایش داده بشه
    readonly_fields = ("datetime_created", "datetime_modified")

    # نمایش عکس کوچک در لیست
    def thumbnail(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="60" height="40" style="object-fit:cover;" />'
        return "-"
    thumbnail.allow_tags = True
    thumbnail.short_description = "Image"
