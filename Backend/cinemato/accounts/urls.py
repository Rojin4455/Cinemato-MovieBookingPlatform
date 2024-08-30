from django.urls import path
from .views import HomeView,RequestOTPView,VerifyOTPView,ResentOtpView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResentOtpView.as_view(), name='verify-otp'),
]