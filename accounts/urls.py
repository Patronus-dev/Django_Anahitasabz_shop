from django.urls import path
from .views import *


urlpatterns = [
    path("login/", PhoneLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("logout/confirm/", TemplateView.as_view(template_name="accounts/logout.html"), name="logout_confirm"),
    path("verify_otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("complete_profile/", CompleteProfileView.as_view(), name="complete_profile"),
    path("resend_otp/", ResendOTPView.as_view(), name="resend_otp"),
    path("user_profile/", UserProfileView.as_view(), name="user_profile"),
    path("edit_profile/", EditProfileView.as_view(), name="edit_profile"),
]
