from django.urls import path
from django.views.generic import RedirectView
from .views import UserListView, ToggleStatusView

app_name = "dashboard"

urlpatterns = [
    path("", RedirectView.as_view(url="users/"), name="index"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<str:user_id>/toggle-status/", ToggleStatusView.as_view(), name="user-toggle-status"),
]
