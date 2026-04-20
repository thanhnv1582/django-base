"""Dashboard presentation views — uses application layer use cases."""
from __future__ import annotations

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest

from apps.users.application.use_cases.list_users import ListUsersUseCase
from apps.users.application.use_cases.toggle_user_status import ToggleUserStatusUseCase, ToggleUserStatusInput
from apps.users.application.dtos.user_dto import ListUsersInput
from apps.users.infrastructure.repositories.django_user_repository import DjangoUserRepository
from apps.users.application.services.unit_of_work import UnitOfWork


def _make_use_cases():
    """Dependency factory — could be improved with DI container."""
    repo = DjangoUserRepository()
    uow = UnitOfWork()
    return ListUsersUseCase(repo=repo), ToggleUserStatusUseCase(repo=repo, uow=uow)


class UserListView(View):
    """Main user management page."""

    def get(self, request: HttpRequest) -> HttpResponse:
        list_use_case, _ = _make_use_cases()
        
        page = int(request.GET.get("page", 1))
        page_size = 10
        
        output = list_use_case.execute(ListUsersInput(page=page, page_size=page_size))
        
        context = {
            "users": output.items,
            "total": output.total,
            "page": output.page,
            "page_size": output.page_size,
            "total_pages": (output.total + page_size - 1) // page_size,
        }
        return render(request, "dashboard/user_list.html", context)


class ToggleStatusView(View):
    """HTMX endpoint to toggle user active status."""

    def post(self, request: HttpRequest, user_id: str) -> HttpResponse:
        _, toggle_use_case = _make_use_cases()
        
        try:
            import uuid
            updated_user = toggle_use_case.execute(ToggleUserStatusInput(user_id=uuid.UUID(user_id)))
            
            # Return only the partial component for the switch/row if needed
            # For simplicity, we return a success indicator or the updated row state
            context = {"user": updated_user}
            return render(request, "dashboard/partials/user_row_status.html", context)
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=400)
