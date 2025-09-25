from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _

from products.models import Product
from .cart import Cart
from .forms import AddToCartProductForm


def cart_detail_view(request):
    cart = Cart(request)

    for item in cart:
        item['product_update_quantity_form'] = AddToCartProductForm(initial={
            'quantity': item['quantity'],
            'inplace': True,   # این فیلد نشون میده فرم مربوط به cart هست نه صفحه محصول
        }, product=item['product_obj'])

    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = AddToCartProductForm(request.POST or None, product=product)

    if request.method == "POST" and form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        inplace = cleaned_data.get('inplace', False)

        # بررسی موجودی نسبت به مجموع در cart
        if inplace:
            if quantity > product.quantity:
                messages.info(request, f"حداکثر تعداد قابل سفارش، {product.quantity} عدد است.")
                return redirect('cart:cart_detail')
        else:
            existing_quantity = cart.cart.get(str(product.id), {}).get('quantity', 0)
            if existing_quantity + quantity > product.quantity:
                messages.info(request, f"حداکثر تعداد قابل سفارش، {product.quantity} عدد است.")
                return redirect(reverse('products:product_detail', args=[product.id]))

        # اضافه یا آپدیت در cart
        cart.add(product, quantity, replace_current_quantity=inplace)

        if inplace:
            messages.info(request, _("The cart has updated."))
            return redirect('cart:cart_detail')
        else:
            messages.success(request, _("The product was successfully added to the cart."))
            return redirect('cart:cart_detail')

    if form.cleaned_data.get('inplace', False):
        return redirect('cart:cart_detail')
    return redirect(reverse('products:product_detail', args=[product.id]))


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.warning(request, _("The product was removed from the cart."))
    return redirect('cart:cart_detail')
