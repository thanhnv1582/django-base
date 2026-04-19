"""URL routes for Users API v1."""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterUserView, UserProfileView

app_name = "users_v1"

urlpatterns = [
    # Auth
    path("auth/register/", RegisterUserView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    # Profile
    path("users/me/", UserProfileView.as_view(), name="profile"),
]
