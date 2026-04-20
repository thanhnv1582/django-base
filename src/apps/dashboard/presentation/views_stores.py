"""Dashboard views for Store management."""
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest

from apps.stores.application.use_cases.list_stores import ListStoresUseCase
from apps.stores.infrastructure.repositories.django_store_repository import DjangoStoreRepository

class StoreListView(View):
    """Main store management page."""

    def get(self, request: HttpRequest) -> HttpResponse:
        repo = DjangoStoreRepository()
        use_case = ListStoresUseCase(store_repo=repo)
        
        stores = use_case.execute()
        
        context = {
            "stores": stores,
        }
        return render(request, "dashboard/stores/list.html", context)
