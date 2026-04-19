"""
API Views for Users v1.

RULES:
- Views ONLY: receive request → call use case → return response
- No business logic here — it belongs in Application layer
- Serializers handle validation, Use Cases handle logic
"""
from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from core.responses.api import success_response
from apps.users.application.dtos.user_dto import RegisterUserInput, UserOutput
from apps.users.application.use_cases.register_user import RegisterUserUseCase
from apps.users.application.use_cases.get_user_profile import GetUserProfileUseCase
from apps.users.application.services.unit_of_work import UnitOfWork
from apps.users.infrastructure.repositories.django_user_repository import DjangoUserRepository
from .serializers import RegisterUserSerializer, UserOutputSerializer


def _make_repo_and_uow():
    """Simple dependency factory — replace with DI container if needed."""
    return DjangoUserRepository(), UnitOfWork()


class RegisterUserView(APIView):
    """POST /api/v1/users/register/ — public endpoint."""

    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterUserSerializer,
        responses={201: UserOutputSerializer},
        description="Register a new user account.",
        tags=["Users"],
    )
    def post(self, request: Request) -> Response:
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo, uow = _make_repo_and_uow()
        use_case = RegisterUserUseCase(repo=repo, uow=uow)

        output: UserOutput = use_case.execute(
            RegisterUserInput(**serializer.validated_data)
        )

        request_id = getattr(request, "request_id", None)
        return Response(
            success_response(
                data=UserOutputSerializer(output).data,
                message="User registered successfully.",
                request_id=request_id,
            ),
            status=status.HTTP_201_CREATED,
        )


class UserProfileView(APIView):
    """GET/PATCH /api/v1/users/me/ — authenticated endpoint."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserOutputSerializer},
        description="Retrieve the authenticated user's profile.",
        tags=["Users"],
    )
    def get(self, request: Request) -> Response:
        repo, _ = _make_repo_and_uow()
        use_case = GetUserProfileUseCase(repo=repo)

        output: UserOutput = use_case.execute(input_dto=request.user.id)

        request_id = getattr(request, "request_id", None)
        return Response(
            success_response(
                data=UserOutputSerializer(output).data,
                request_id=request_id,
            )
        )
