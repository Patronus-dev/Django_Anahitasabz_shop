from django.views.generic import ListView, DetailView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(active=True).order_by('-datetime_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']

        start = max(page_obj.number - 2, 1)
        end = min(page_obj.number + 2, paginator.num_pages)
        context['page_range_limited'] = range(start, end + 1)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # محصولات مشابه بر اساس کلیدواژه‌ها
        similar_products = Product.objects.filter(
            keywords__in=product.keywords.all()
        ).exclude(pk=product.pk).distinct()[:4]

        # اگر محصول مشابه وجود نداشت، آخرین محصولات فعال به غیر از محصول جاری
        if not similar_products.exists():
            similar_products = Product.objects.filter(active=True).exclude(pk=product.pk).order_by('-datetime_created')[
                               :4]

        context['similar_products'] = similar_products
        return context
