from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import FormView, DetailView, TemplateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import random

from .models import CustomUser, OTP
from .forms import PhoneLoginForm, VerifyOTPForm, CompleteProfileForm, UserUpdateForm
from orders.models import Order


class PhoneLoginView(FormView):
    template_name = "accounts/phone_login.html"
    form_class = PhoneLoginForm
    success_url = reverse_lazy("accounts:verify_otp")

    def form_valid(self, form):
        phone = form.cleaned_data["phone"]

        user, created = CustomUser.objects.get_or_create(username=phone)

        code = f"{random.randint(1000, 9999)}"
        OTP.objects.create(user=user, code=code)

        print(f"OTP برای {phone}: {code}")

        self.request.session["otp_user_id"] = user.id
        self.request.session["is_new_user"] = created

        return super().form_valid(form)


class VerifyOTPView(FormView):
    template_name = "accounts/verify_otp.html"
    form_class = VerifyOTPForm

    def get_success_url(self):
        if self.request.session.get("is_new_user", False):
            return reverse_lazy("accounts:complete_profile")
        return reverse_lazy("home")

    def form_valid(self, form):
        user_id = self.request.session.get("otp_user_id")
        if not user_id:
            return redirect("accounts:login")

        user = CustomUser.objects.get(id=user_id)
        code = form.cleaned_data["code"]

        otp_obj = OTP.objects.filter(user=user).order_by("-created_at").first()

        if not otp_obj or otp_obj.code != code:
            form.add_error("code", "کد وارد شده نامعتبر است.")
            return self.form_invalid(form)

        if timezone.now() - otp_obj.created_at > timedelta(minutes=2):
            form.add_error("code", "کد منقضی شده است.")
            return self.form_invalid(form)

        if self.request.session.get("is_new_user", False):
            self.request.session["pending_phone"] = user.username
        else:
            login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        return super().form_valid(form)


class CompleteProfileView(FormView):
    template_name = "accounts/complete_profile.html"
    form_class = CompleteProfileForm
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

        for field, value in form.cleaned_data.items():
            setattr(user, field, value)

        user.save()

        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        self.request.session.pop("pending_phone", None)

        return super().form_valid(form)


class ResendOTPView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.session.get("otp_user_id")

        if not user_id:
            return JsonResponse(
                {"success": False, "message": "Session expired"},
                status=400
            )

        user = CustomUser.objects.get(id=user_id)

        last_otp = OTP.objects.filter(user=user).order_by("-created_at").first()

        # جلوگیری از ارسال پشت سر هم (30 ثانیه)
        if last_otp and timezone.now() - last_otp.created_at < timedelta(seconds=30):
            return JsonResponse(
                {"success": False, "message": "لطفاً کمی صبر کنید"},
                status=429
            )

        code = f"{random.randint(1000, 9999)}"
        OTP.objects.create(user=user, code=code)

        print(f"OTP جدید برای {user.username}: {code}")

        return JsonResponse({
            "success": True,
            "message": "کد جدید ارسال شد"
        })


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "accounts/user_profile.html"
    context_object_name = "user_profile"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-datetime_created')
        return context


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
    success_url = reverse_lazy("accounts:user_profile")

    def get_object(self, queryset=None):
        return self.request.user