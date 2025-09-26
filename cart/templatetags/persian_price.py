from django import template

register = template.Library()

PERSIAN_NUMS = {
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹',
}


@register.filter
def price_fa(value):
    """
    جدا کردن سه رقم سه رقم و تبدیل اعداد به فارسی
    فقط برای مقادیر پولی استفاده شود
    """
    try:
        value = int(value)
        s = f"{value:,}"  # جدا کردن سه رقم سه رقم
        for en, fa in PERSIAN_NUMS.items():
            s = s.replace(en, fa)
        return s
    except (ValueError, TypeError):
        return value
