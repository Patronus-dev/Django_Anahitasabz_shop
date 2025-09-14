import re
from django.utils.deprecation import MiddlewareMixin

PERSIAN_DIGITS = {
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

def convert_to_persian(text):
    for en, fa in PERSIAN_DIGITS.items():
        text = text.replace(en, fa)
    return text


class PersianDigitsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        content_type = response.get('Content-Type', '')

        # فقط HTML ها رو تغییر بده
        if content_type.startswith('text/html'):
            try:
                content = response.content.decode('utf-8')

                # ❌ فیلدهای input hidden (مثلاً csrfmiddlewaretoken) رو تغییر نده
                def safe_replace(match):
                    tag = match.group(0)
                    if 'type="hidden"' in tag or 'csrfmiddlewaretoken' in tag:
                        return tag  # دست نزن
                    return convert_to_persian(tag)

                # فقط محتوای بین تگ‌ها رو تغییر بده
                content = re.sub(r'>([^<]+)<', lambda m: ">" + convert_to_persian(m.group(1)) + "<", content)

                response.content = content.encode('utf-8')
            except Exception as e:
                pass

        return response
