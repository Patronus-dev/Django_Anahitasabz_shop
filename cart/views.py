from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from products.models import Product
from .cart import Cart
from .models import Coupon, Shipping
from .forms import AddToCartProductForm, CouponForm


def cart_detail_view(request):
    """
    نمایش جزئیات سبد خرید
    """
    cart = Cart(request)

    # اگر سبد خرید خالی است، کوپن را پاک کن
    if len(cart) == 0 and 'coupon' in request.session:
        del request.session['coupon']

    coupon_form = CouponForm()

    for item in cart:
        item['product_update_quantity_form'] = AddToCartProductForm(
            initial={'quantity': item['quantity'], 'inplace': True},
            product=item['product_obj']
        )

    # جمع محصولات بدون اعشار
    products_total = sum(int(item['product_obj'].price * item['quantity']) for item in cart)

    # لیست روش‌های ارسال فعال
    shippings = Shipping.objects.filter(active=True)

    # روش ارسال انتخاب‌شده
    shipping_id = request.session.get('shipping_id')
    selected_shipping = None
    shipping_cost = 0

    if shipping_id:
        selected_shipping = Shipping.objects.filter(id=shipping_id, active=True).first()
    elif shippings.exists():
        selected_shipping = shippings.first()  # پیش‌فرض روی اولین روش فعال

    if selected_shipping and not getattr(selected_shipping, 'cost_on_delivery', False):
        shipping_cost = int(selected_shipping.cost)

    # مقدار و نوع تخفیف
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
            coupon_display = f"{coupon_value} {_('Toman')}"

    # جمع کل نهایی
    total = (products_total - coupon_value) + shipping_cost
    if total < 0:
        total = 0

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'coupon_form': coupon_form,
        'products_total': products_total,
        'shipping_cost': shipping_cost,
        'total': total,
        'coupon_value': coupon_value,
        'coupon_display': coupon_display,
        'shippings': shippings,
        'selected_shipping': selected_shipping,
    })


@require_POST
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST, product=product)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        inplace = form.cleaned_data.get('inplace', False)
        cart.add(product, quantity, replace_current_quantity=inplace)
        if inplace:
            messages.info(request, _("The cart has been updated."))
        else:
            messages.success(request, _("The product was successfully added to the cart."))
    else:
        messages.warning(request, _("Something went wrong while adding to cart."))

    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    # اگر سبد خالی شد، کوپن پاک شود
    if len(cart) == 0 and 'coupon' in request.session:
        del request.session['coupon']

    messages.warning(request, _("The product was removed from the cart."))
    return redirect('cart:cart_detail')


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()

    # پاک کردن کوپن هنگام خالی شدن سبد
    if 'coupon' in request.session:
        del request.session['coupon']

    messages.success(request, _("The cart has been cleared."))
    return redirect('cart:cart_detail')


@require_POST
def apply_coupon(request):
    if not request.user.is_authenticated:
        messages.warning(request, _("You need to login to use a coupon."))
        return redirect('cart:cart_detail')

    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)

            # بررسی منقضی شدن کوپن
            if coupon.datetime_expired and coupon.datetime_expired < timezone.now():
                messages.warning(request, _("This coupon has expired."))
                return redirect('cart:cart_detail')

            # بررسی استفاده قبلی کاربر
            if request.user in coupon.used_by.all():
                messages.warning(request, _("You have already used this coupon."))
                return redirect('cart:cart_detail')

            # ذخیره کوپن در سشن تا خرید انجام نشده اعمال شود
            request.session['coupon'] = {
                'code': coupon.code,
                'discount_type': coupon.discount_type,
                'discount_value': float(coupon.discount_value),
            }
            messages.success(request, _("Coupon applied successfully!"))

        except Coupon.DoesNotExist:
            messages.warning(request, _("The Coupon code is invalid or expired."))

    return redirect('cart:cart_detail')


@require_POST
def set_shipping(request):
    shipping_id = request.POST.get('shipping_id')
    shipping = Shipping.objects.filter(id=shipping_id, active=True).first()
    if shipping:
        request.session['shipping_id'] = shipping.id
        # هزینه ارسال فقط اگر روش پرداخت توسط گیرنده نباشد
        request.session['shipping_cost'] = 0 if getattr(shipping, 'cost_on_delivery', False) else shipping.cost
        messages.success(request, _("Shipping method updated!"))
    else:
        request.session['shipping_cost'] = 0
        messages.warning(request, _("Invalid shipping method."))
    return redirect('cart:cart_detail')


