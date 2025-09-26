from .cart import Cart


def cart_context(request):
    cart = Cart(request)
    return {
        'cart': cart,  # کل سبد خرید
        'cart_item_count': len(cart)  # تعداد آیتم‌ها
    }
