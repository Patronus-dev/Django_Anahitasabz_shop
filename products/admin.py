from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import Product, Keyword, Category


class ProductAdminForm(forms.ModelForm):
    keyword_text = forms.CharField(
        required=False,
        label="Keywords",
        help_text="کلمات کلیدی را با علامت کاما ( , ) جدا کنید"
    )

    class Meta:
        model = Product
        fields = '__all__'   # بهتر از exclude برای آینده

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Keywords initial
        if self.instance.pk:
            self.fields['keyword_text'].initial = ", ".join(
                [kw.name for kw in self.instance.keywords.all()]
            )

        # Category initial
        if self.instance.pk and self.instance.category:
            self.fields['category'].initial = self.instance.category

    def save(self, commit=True):
        instance = super().save(commit=False)

        # پردازش keywords
        keywords_str = self.cleaned_data.get('keyword_text', '')
        keyword_names = [k.strip() for k in keywords_str.split(",") if k.strip()]

        keywords_objs = []
        for name in keyword_names:
            kw_obj, _ = Keyword.objects.get_or_create(name=name)
            keywords_objs.append(kw_obj)

        if commit:
            instance.save()
            instance.keywords.set(keywords_objs)
        else:
            self._pending_keywords = keywords_objs

        return instance


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = (
        'title',
        'category',
        'quantity',
        'price',
        'active',
        'datetime_created',
        'datetime_modified',
        'cover_preview',
        'display_keywords',
    )

    list_filter = (
        'active',
        'category',
        'datetime_created',
        'datetime_modified',
    )

    search_fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # sync keywords after save
        if hasattr(form, '_pending_keywords'):
            obj.keywords.set(form._pending_keywords)

    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="width:50px; height:auto;" />',
                obj.cover.url
            )
        return "-"
    cover_preview.short_description = "Cover"

    def display_keywords(self, obj):
        return ", ".join([kw.name for kw in obj.keywords.all()])
    display_keywords.short_description = "Keywords"


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)
