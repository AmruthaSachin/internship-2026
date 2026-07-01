from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, LoginView, test_email, SendOTPView, VerifyOTPView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test-email/', test_email, name='test-email'),
    path('send-otp/',SendOTPView.as_view(),name='send-otp'),
    path('verify-otp/',VerifyOTPView.as_view(),name='verify-otp'),
]
