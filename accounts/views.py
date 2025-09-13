from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import FormView, DetailView, TemplateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
import random
from django.http import JsonResponse
from django.contrib.auth import logout

from .models import CustomUser, OTP
from .forms import PhoneLoginForm, VerifyOTPForm, CompleteProfileForm, UserUpdateForm


class PhoneLoginView(FormView):
    template_name = "accounts/phone_login.html"
    form_class = PhoneLoginForm
    success_url = reverse_lazy("verify_otp")

    def form_valid(self, form):
        phone = form.cleaned_data["phone"]

        # اگر کاربر وجود داشته باشه بگیر، وگرنه بساز
        user, created = CustomUser.objects.get_or_create(username=phone)

        # تولید OTP چهاررقمی
        code = f"{random.randint(1000, 9999)}"
        OTP.objects.create(user=user, code=code)
        print(f"OTP برای {phone}: {code}")  # فقط برای تست

        # ذخیره در session
        self.request.session["otp_user_id"] = user.id
        self.request.session["is_new_user"] = created

        return super().form_valid(form)


class VerifyOTPView(FormView):
    template_name = "accounts/verify_otp.html"
    form_class = VerifyOTPForm

    def get_success_url(self):
        # کاربر جدید → تکمیل پروفایل
        if self.request.session.get("is_new_user", False):
            return reverse_lazy("complete_profile")
        # کاربر قدیمی → home
        return reverse_lazy("home")

    def form_valid(self, form):
        user_id = self.request.session.get("otp_user_id")
        if not user_id:
            return redirect("phone_login")

        user = CustomUser.objects.get(id=user_id)
        code = form.cleaned_data["code"]

        # بررسی OTP
        try:
            otp_obj = OTP.objects.filter(user=user, code=code).latest("created_at")
        except OTP.DoesNotExist:
            form.add_error("code", "کد وارد شده نامعتبر است.")
            return self.form_invalid(form)

        if otp_obj.is_expired():
            form.add_error("code", "کد وارد شده منقضی شده است.")
            return self.form_invalid(form)

        # کاربر جدید → هدایت به تکمیل پروفایل
        if self.request.session.get("is_new_user", False):
            self.request.session["pending_phone"] = user.username
        else:
            # کاربر قدیمی → لاگین و هدایت به home
            login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        return super().form_valid(form)


class CompleteProfileView(FormView):
    template_name = "accounts/complete_profile.html"
    form_class = CompleteProfileForm  # استفاده از فرم جدید
    success_url = reverse_lazy("home")

    def get_initial(self):
        phone = self.request.session.get("pending_phone")
        if phone:
            user = CustomUser.objects.get(username=phone)
            return {
                "name": user.name,
                "lastname": user.lastname,
                "province": user.province,
                "city": user.city,
                "address": user.address,
                "postal_code": user.postal_code,
            }
        return super().get_initial()

    def form_valid(self, form):
        phone = self.request.session.get("pending_phone")
        user = CustomUser.objects.get(username=phone)

        # به‌روزرسانی اطلاعات کاربر
        for field, value in form.cleaned_data.items():
            setattr(user, field, value)
        user.save()

        # لاگین و حذف session
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        self.request.session.pop("pending_phone", None)

        return super().form_valid(form)


class ResendOTPView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.session.get("otp_user_id")
        if not user_id:
            return JsonResponse({"success": False, "message": "User not found in session."})

        user = CustomUser.objects.get(id=user_id)

        # ساخت OTP جدید
        code = f"{random.randint(1000, 9999)}"
        OTP.objects.create(user=user, code=code)

        # TODO: ارسال پیامک واقعی
        print(f"OTP جدید برای {user.username}: {code}")  # فقط برای تست

        return JsonResponse({"success": True, "message": "کد جدید ارسال شد."})


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "accounts/user_profile.html"
    context_object_name = "user_profile"

    def get_object(self):
        return self.request.user


class CustomLogoutConfirmView(TemplateView):
    template_name = "accounts/logout.html"


class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy("user_profile")  # بعد از ذخیره به پروفایل هدایت شود

    def get_object(self, queryset=None):
        # کاربر فعلی را برمی‌گرداند
        return self.request.user