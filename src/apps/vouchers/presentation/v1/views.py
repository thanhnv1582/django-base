from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.vouchers.infrastructure.repositories.django_voucher_repository import DjangoVoucherRepository
from apps.vouchers.application.use_cases.create_voucher import CreateVoucherUseCase, CreateVoucherDTO
from apps.vouchers.application.use_cases.list_vouchers import ListVouchersUseCase
from apps.vouchers.presentation.v1.serializers import VoucherSerializer

class VoucherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Vouchers.
    """
    serializer_class = VoucherSerializer
    repository = DjangoVoucherRepository()

    def get_queryset(self):
        # In a real app, we would filter by the user's store permissions
        from apps.vouchers.models import Voucher
        return Voucher.objects.all()

    def create(self, request, *args, **kwargs):
        use_case = CreateVoucherUseCase(self.repository)
        try:
            dto = CreateVoucherDTO(
                code=request.data.get("code"),
                voucher_type=request.data.get("voucher_type"),
                value=float(request.data.get("value")),
                store_id=request.data.get("store"),
                min_order_value=float(request.data.get("min_order_value", 0)),
                max_discount_amount=request.data.get("max_discount_amount"),
                usage_limit=int(request.data.get("usage_limit", 0)),
                usage_per_user=int(request.data.get("usage_per_user", 1)),
                start_date=request.data.get("start_date"),
                end_date=request.data.get("end_date")
            )
            entity = use_case.execute(dto)
            
            # Map back to model for serialization
            from apps.vouchers.models import Voucher
            model = Voucher.objects.get(id=entity.id)
            serializer = self.get_serializer(model)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="store/(?P<store_id>[^/.]+)")
    def list_by_store(self, request, store_id=None):
        use_case = ListVouchersUseCase(self.repository)
        entities = use_case.execute(store_id)
        
        from apps.vouchers.models import Voucher
        models = Voucher.objects.filter(id__in=[e.id for e in entities])
        serializer = self.get_serializer(models, many=True)
        return Response(serializer.data)
