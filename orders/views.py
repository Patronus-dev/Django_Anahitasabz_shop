from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.cart import Cart
from cart.models import Shipping
from .forms import CheckoutUserForm
from .models import Order, OrderItem


def calculate_order_totals(request, cart):
    """محاسبه جمع کل سفارش + کوپن + هزینه ارسال"""
    products_total = sum(int(item['product_obj'].price * item['quantity']) for item in cart)

    # روش ارسال
    shipping_id = request.session.get("shipping_id")
    selected_shipping = Shipping.objects.filter(id=shipping_id, active=True).first()
    shipping_cost = int(selected_shipping.cost) if selected_shipping else 0

    # کوپن
    coupon_value = 0
    coupon_code = None
    coupon_display = None
    coupon_data = request.session.get("coupon")
    if coupon_data:
        coupon_code = coupon_data.get("code")
        if coupon_data['discount_type'] == 'percent':
            percent = float(coupon_data['discount_value'])
            coupon_value = int(products_total * percent / 100)
            coupon_display = f"{int(percent)} %"
        else:
            coupon_value = int(float(coupon_data['discount_value']))
            coupon_display = f"{coupon_value}"

    # جمع کل
    total = (products_total - coupon_value) + shipping_cost
    if total < 0:
        total = 0

    return {
        "products_total": products_total,
        "shipping_cost": shipping_cost,
        "total": total,
        "coupon_value": coupon_value,
        "coupon_code": coupon_code,
        "coupon_display": coupon_display,
        "selected_shipping": selected_shipping,
    }


@login_required
def checkout_view(request):
    cart = Cart(request)
    user = request.user

    if request.method == "POST":
        form = CheckoutUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            totals = calculate_order_totals(request, cart)

            # ساخت سفارش با ذخیره اطلاعات کامل
            order = Order.objects.create(
                user=user,
                total_price=totals["total"],
                shipping_method=totals["selected_shipping"],
                coupon_code=totals["coupon_code"],
                order_notes=form.cleaned_data.get("order_notes", "")
            )

            # ذخیره آیتم‌های سفارش
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product_obj"],
                    price=item["product_obj"].price,
                    quantity=item["quantity"],
                )

            # پاک کردن سبد و کوپن
            cart.clear()
            request.session.pop("coupon", None)

            messages.success(request, "Your order has been successfully placed! ✅")
            return redirect("orders:order_detail", order_id=order.id)
        else:
            messages.info(request, "The information entered is not valid.")
    else:
        form = CheckoutUserForm(instance=user)

    # ---- GET: نمایش صفحه چک‌اوت ----
    totals = calculate_order_totals(request, cart)
    shippings = Shipping.objects.filter(active=True)

    context = {
        'cart': cart,
        'checkout_form': form,
        'products_total': totals["products_total"],
        'shipping_cost': totals["shipping_cost"],
        'total': totals["total"],
        'coupon_value': totals["coupon_value"],
        'coupon_display': totals["coupon_display"],
        'shippings': shippings,
        'selected_shipping': totals["selected_shipping"],
    }
    return render(request, 'orders/order_create.html', context)
