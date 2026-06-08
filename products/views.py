from django.shortcuts import render
from django.views.generic import *
from django.db.models import Q

from .models import Product
from cart.forms import AddToCartProductForm


def get_category_breadcrumb(category):
    breadcrumb = []

    while category:
        breadcrumb.append({
            "title": category.name,
            "url": f"/products/category/{category.slug}/"
        })
        category = category.parent

    breadcrumb.reverse()
    return breadcrumb


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

        # breadcrumb
        context['breadcrumb'] = [
            {"title": "محصولات", "url": None}
        ]

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

        # breadcrumb base
        breadcrumb = [
            {"title": "محصولات", "url": "/products/"},
        ]

        # category hierarchy
        if product.category:
            breadcrumb += get_category_breadcrumb(product.category)

        # current product
        breadcrumb.append({
            "title": product.title,
            "url": None
        })

        context['breadcrumb'] = breadcrumb

        # similar products
        keywords = product.keywords.all()

        if keywords.exists():
            similar_products = Product.objects.filter(
                active=True,
                keywords__in=keywords
            ).exclude(id=product.id).distinct()[:8]
        else:
            similar_products = Product.objects.filter(
                active=True
            ).exclude(id=product.id)[:8]

        context['similar_products'] = similar_products

        return context


# ویو برای جستجو
def product_search_view(request):
    user_search = request.GET.get('q', '')

    products = Product.objects.filter(
        Q(title__icontains=user_search) |
        Q(description__icontains=user_search) |
        Q(keywords__name__icontains=user_search),
        active=True
    ).distinct() if user_search else []

    context = {
        'user_search': user_search,
        'products': products,
        'breadcrumb': [
            {"title": "جستجو", "url": None}
        ]}

    # breadcrumb

    return render(request, 'pages/search_result.html', context)
