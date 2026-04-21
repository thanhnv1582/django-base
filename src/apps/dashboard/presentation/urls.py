from django.urls import path
from django.views.generic import RedirectView
from .views import UserListView, ToggleStatusView
from .views_stores import StoreListView
from .views_vouchers import VoucherListView, VoucherCreateView

app_name = "dashboard"

urlpatterns = [
    path("", RedirectView.as_view(url="users/"), name="index"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<str:user_id>/toggle-status/", ToggleStatusView.as_view(), name="user-toggle-status"),
    path("stores/", StoreListView.as_view(), name="store-list"),
    path("vouchers/", VoucherListView.as_view(), name="voucher-list"),
    path("vouchers/create/", VoucherCreateView.as_view(), name="voucher-create"),
]
