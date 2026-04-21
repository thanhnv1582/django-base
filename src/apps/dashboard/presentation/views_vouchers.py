"""Dashboard views for Voucher management."""
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpRequest
from django.urls import reverse

from apps.vouchers.application.use_cases.list_vouchers import ListVouchersUseCase
from apps.vouchers.application.use_cases.create_voucher import CreateVoucherUseCase, CreateVoucherDTO
from apps.vouchers.infrastructure.repositories.django_voucher_repository import DjangoVoucherRepository
from apps.stores.infrastructure.repositories.django_store_repository import DjangoStoreRepository
from apps.stores.application.use_cases.list_stores import ListStoresUseCase

class VoucherListView(View):
    """Main voucher management page."""

    def get(self, request: HttpRequest) -> HttpResponse:
        voucher_repo = DjangoVoucherRepository()
        store_repo = DjangoStoreRepository()
        
        # For simplicity, we list vouchers for the first store if store_id not provided
        # In a real app, this would be based on the selected store in the session/header
        stores = ListStoresUseCase(store_repo).execute()
        store_id = request.GET.get("store_id")
        
        if not store_id and stores:
            store_id = str(stores[0].id)
            
        vouchers = []
        if store_id:
            vouchers = ListVouchersUseCase(voucher_repo).execute(store_id)
            
        context = {
            "vouchers": vouchers,
            "stores": stores,
            "selected_store_id": store_id,
        }
        return render(request, "dashboard/vouchers/list.html", context)

class VoucherCreateView(View):
    """HTMX view to handle voucher creation."""
    
    def post(self, request: HttpRequest) -> HttpResponse:
        repo = DjangoVoucherRepository()
        use_case = CreateVoucherUseCase(repo)
        
        try:
            dto = CreateVoucherDTO(
                code=request.POST.get("code"),
                voucher_type=request.POST.get("voucher_type"),
                value=float(request.POST.get("value")),
                store_id=request.POST.get("store_id"),
                min_order_value=float(request.POST.get("min_order_value", 0)),
                usage_limit=int(request.POST.get("usage_limit", 0)),
                start_date=None, # Will use default
                end_date=None    # Will use default (6 months)
            )
            use_case.execute(dto)
            
            # Redirect back to list or return success
            return HttpResponse(status=204, headers={"HX-Trigger": "voucherListChanged"})
        except Exception as e:
            return HttpResponse(f'<div class="text-red-500">Error: {e}</div>', status=400)
