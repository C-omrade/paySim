from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated 

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Payment.objects.select_related(
            "merchant",
            "customer",
        ).all()

        payment_status = self.request.query_params.get("status")
        customer_id = self.request.query_params.get("customer_id")
        merchant_id = self.request.query_params.get("merchant_id")

        if payment_status:
            queryset = queryset.filter(status=payment_status.upper())

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)

        if merchant_id:
            queryset = queryset.filter(merchant_id=merchant_id)

        return queryset.order_by("-created_at")