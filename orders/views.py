from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from cart.cart import Cart
from cart.models import Shipping
from .forms import CheckoutUserForm


def checkout_view(request):
    cart = Cart(request)
    user = request.user if request.user.is_authenticated else None

    # فرم کاربر
    if user:
        form = CheckoutUserForm(instance=user)
    else:
        form = CheckoutUserForm()

    # جمع محصولات
    products_total = sum(int(item['product_obj'].price * item['quantity']) for item in cart)

    # روش‌های ارسال فعال
    shippings = Shipping.objects.filter(active=True)

    # روش انتخاب‌شده
    shipping_id = request.session.get('shipping_id')
    selected_shipping = None
    shipping_cost = 0

    if shipping_id:
        selected_shipping = Shipping.objects.filter(id=shipping_id, active=True).first()
    elif shippings.exists():
        selected_shipping = shippings.first()

    if selected_shipping and not getattr(selected_shipping, 'cost_on_delivery', False):
        shipping_cost = int(selected_shipping.cost)

    # بررسی کوپن
    coupon_value = 0
    coupon_display = None
    coupon_data = request.session.get('coupon')

    if coupon_data:
        if coupon_data['discount_type'] == 'percent':
            percent = float(coupon_data['discount_value'])
            coupon_value = int(products_total * percent / 100)
            coupon_display = f"{int(percent)} %"
        else:  # fixed amount
            coupon_value = int(float(coupon_data['discount_value']))
            coupon_display = f"{coupon_value}"

    # جمع کل نهایی
    total = (products_total - coupon_value) + shipping_cost
    if total < 0:
        total = 0

    context = {
        'cart': cart,
        'checkout_form': form,
        'products_total': products_total,
        'shipping_cost': shipping_cost,
        'total': total,
        'coupon_value': coupon_value,
        'coupon_display': coupon_display,
        'shippings': shippings,
        'selected_shipping': selected_shipping,
    }
    return render(request, 'orders/order_create.html', context)
