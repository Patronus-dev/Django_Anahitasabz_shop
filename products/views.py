from django.views.generic import ListView, DetailView
from .models import Product
from cart.forms import AddToCartProductForm


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

        # فرم اضافه به سبد خرید
        context['add_to_cart_form'] = AddToCartProductForm(product=product)

        # گرفتن کلیدواژه‌های محصول جاری
        keywords = product.keywords.all()

        if keywords.exists():
            # گرفتن محصولات مشابه که حداقل یک کلیدواژه مشترک داشته باشن
            similar_products = Product.objects.filter(
                active=True,
                keywords__in=keywords
            ).exclude(id=product.id).distinct()[:8]
        else:
            # اگر محصول کلیدواژه نداشت، سایر محصولات فعال رو نشون بده
            similar_products = Product.objects.filter(active=True).exclude(id=product.id)[:8]

        context['similar_products'] = similar_products

        return context

