from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.vouchers.presentation.v1.views import VoucherViewSet

router = DefaultRouter()
router.register(r'', VoucherViewSet, basename='voucher')

urlpatterns = [
    path('', include(router.urls)),
]
