"""
API Views for Stores v1.
"""
from __future__ import annotations

import uuid
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.responses.api import success_response
from apps.stores.application.dtos.store_dtos import StoreCreateDTO
from apps.stores.application.use_cases.create_store import CreateStoreUseCase
from apps.stores.infrastructure.repositories.django_store_repository import DjangoStoreRepository
from .serializers import StoreSerializer

def _make_repo():
    return DjangoStoreRepository()

class StoreListView(APIView):
    """
    GET /api/v1/stores/ - List all active stores.
    POST /api/v1/stores/ - Create a new store.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: StoreSerializer(many=True)},
        description="List all active stores.",
        tags=["Stores"],
    )
    def get(self, request: Request) -> Response:
        repo = _make_repo()
        stores = repo.list_all(is_active=True)
        data = [StoreSerializer(s).data for s in stores]
        return Response(success_response(data=data))

    @extend_schema(
        request=StoreSerializer,
        responses={201: StoreSerializer},
        description="Create a new store.",
        tags=["Stores"],
    )
    def post(self, request: Request) -> Response:
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = _make_repo()
        use_case = CreateStoreUseCase(store_repo=repo)

        input_dto = StoreCreateDTO(**serializer.validated_data)
        
        # Ensure user_id is a UUID object
        user_id = request.user.id
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)

        output = use_case.execute(input_dto=input_dto, user_id=user_id)
        
        # Use serializer to convert DTO/Model to dict for Response
        data = StoreSerializer(output).data

        return Response(
            success_response(data=data, message="Store created successfully."),
            status=status.HTTP_201_CREATED
        )

class MyStoresView(APIView):
    """
    GET /api/v1/stores/my/ - List stores where current user is a member.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: StoreSerializer(many=True)},
        description="List stores associated with the current user.",
        tags=["Stores"],
    )
    def get(self, request: Request) -> Response:
        repo = _make_repo()
        
        user_id = request.user.id
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)

        stores = repo.get_user_stores(user_id=user_id)
        data = [StoreSerializer(s).data for s in stores]
        return Response(success_response(data=data))
