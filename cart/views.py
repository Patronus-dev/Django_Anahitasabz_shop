from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from products.models import Product
from .cart import Cart
from .forms import AddToCartProductForm


def cart_detail_view(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = AddToCartProductForm(request.POST or None, product=product)

    if request.method == "POST" and form.is_valid():
        quantity = form.cleaned_data['quantity']

        if product.quantity >= quantity:
            cart.add(product, quantity)
            product.quantity -= quantity
            product.save()
            return redirect('cart:cart_detail')
        else:
            form.add_error('quantity', "موجودی کافی نیست")

    return redirect(reverse('products:product_detail', args=[product.id]))
