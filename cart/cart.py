from products.models import Product


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self.session.get('cart', {})
        self.coupon = self.session.get('coupon', None)

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
        اضافه کردن محصول به سبد خرید یا آپدیت تعداد آن
        """
        product_id = str(product.id)
        current_quantity = self.cart.get(product_id, {}).get('quantity', 0)

        if replace_current_quantity:
            new_quantity = quantity
        else:
            new_quantity = current_quantity + quantity

        # محدود کردن تعداد به موجودی محصول
        new_quantity = min(new_quantity, product.quantity)

        self.cart[product_id] = {'quantity': new_quantity}
        self.save()

    def remove(self, product):
        """حذف محصول از سبد"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """پاک کردن کامل سبد و کوپن"""
        self.cart = {}
        self.coupon = None
        self.save()

    def apply_coupon(self, coupon):
        """
        ذخیره کوپن در سشن
        coupon: dict یا object با فیلدهای code, discount_type, discount_value
        """
        self.coupon = {
            'code': coupon['code'],
            'discount_type': coupon['discount_type'],
            'discount_value': float(coupon['discount_value']),
        }
        self.save()

    def remove_coupon(self):
        """حذف کوپن از سبد"""
        self.coupon = None
        self.save()

    def save(self):
        """ذخیره تغییرات در سشن"""
        self.session['cart'] = self.cart
        if self.coupon:
            self.session['coupon'] = self.coupon
        else:
            self.session.pop('coupon', None)
        self.session.modified = True

    def __iter__(self):
        """تولید آیتم‌های سبد با اطلاعات محصول و قیمت کل هر محصول"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_copy = self.cart.copy()

        for product in products:
            cart_copy[str(product.id)]['product_obj'] = product

        for item in cart_copy.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        """تعداد کل آیتم‌ها در سبد"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self, shipping_cost=0):
        """
        جمع کل سبد خرید
        shipping_cost: هزینه حمل به تومان
        """
        total = sum(item['quantity'] * item['product_obj'].price for item in self)

        # اعمال کوپن
        if self.coupon:
            if self.coupon['discount_type'] == 'percent':
                total -= total * (self.coupon['discount_value'] / 100)
            else:  # fixed amount
                total -= self.coupon['discount_value']

            total = max(total, 0)  # جلوگیری از منفی شدن

        # جمع هزینه حمل
        total += shipping_cost

        return total


