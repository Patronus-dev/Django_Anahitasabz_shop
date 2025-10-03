from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime
import jdatetime

from cart.cart import Cart
from cart.models import Shipping, Coupon
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
def order_create_view(request):
    cart = Cart(request)
    user = request.user

    # جلوگیری از ثبت سفارش وقتی سبد خرید خالیه
    if len(cart) == 0:
        messages.warning(request, _("Your cart is empty. You cannot checkout without products."))
        return redirect("products:product_list")

    if request.method == "POST":
        form = CheckoutUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            # قبل از ساخت سفارش، بررسی موجودی کالاها
            for item in cart:
                product = item['product_obj']
                if item['quantity'] > product.quantity:
                    messages.warning(
                        request,
                        _("There is not enough stock. Please check the product page again.")
                    )
                    return redirect("cart:cart_detail")

            totals = calculate_order_totals(request, cart)

            # ساخت سفارش
            order = Order.objects.create(
                user=user,
                total_price=totals["total"],
                shipping_method=totals["selected_shipping"],
                coupon_code=totals["coupon_code"],
                coupon_value=totals["coupon_value"],
                coupon_display=totals["coupon_display"],
                order_notes=form.cleaned_data.get("order_notes", "")
            )

            # ذخیره آیتم‌های سفارش و کاهش موجودی محصول
            for item in cart:
                product = item["product_obj"]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item["quantity"],
                )

                # کاهش موجودی
                product.quantity -= item["quantity"]
                if product.quantity < 0:
                    product.quantity = 0  # جلوگیری از منفی شدن موجودی
                product.save()

            # اگر کوپن استفاده شده بود → به used_by اضافه کن
            coupon_data = request.session.get("coupon")
            if coupon_data:
                try:
                    coupon = Coupon.objects.get(code=coupon_data["code"])
                    coupon.used_by.add(user)
                except Coupon.DoesNotExist:
                    pass

            # پاک کردن سبد و کوپن
            cart.clear()
            request.session.pop("coupon", None)

            messages.success(request, _("Your order has been successfully placed! ✅"))

            return redirect("orders:order_detail", order_id=order.id)

        else:
            messages.info(request, _("The information entered is not valid."))
    else:
        form = CheckoutUserForm(instance=user)

    totals = calculate_order_totals(request, cart)
    shippings = Shipping.objects.filter(active=True)

    context = {
        "cart": cart,
        "checkout_form": form,
        "products_total": totals["products_total"],
        "shipping_cost": totals["shipping_cost"],
        "total": totals["total"],
        "coupon_value": totals["coupon_value"],
        "coupon_display": totals["coupon_display"],
        "shippings": shippings,
        "selected_shipping": totals["selected_shipping"],
    }
    return render(request, "orders/order_create.html", context)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    pk_url_kwarg = 'order_id'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()

        # تاریخ ایجاد سفارش به شمسی
        jalali_date = jdatetime.datetime.fromgregorian(datetime=localtime(order.datetime_created))

        # شماره سفارش اختصاصی
        context['order_number'] = f"00{jalali_date.strftime('%Y%m%d')}{order.id}"

        # جمع محصولات بدون تخفیف و ارسال
        products_total = sum(item.price * item.quantity for item in order.items.all())
        context['products_total'] = products_total
        return context
