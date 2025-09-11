from django.urls import path
from .views import *


urlpatterns = [
    path("login/", PhoneLoginView.as_view(), name="login"),
    path("verify_otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("complete_profile/", CompleteProfileView.as_view(), name="complete_profile"),
    path("resend_otp/", ResendOTPView.as_view(), name="resend_otp"),
]
