from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from .models import Merchant
from django.utils import timezone
from rest_framework.response import Response
from .serializers import MerchantSerializer

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.select_related("user").all()
    serializer_class = MerchantSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        merchant = self.get_object()
        merchant.status = 'approved'
        # merchant.approved_by = request.user
        merchant.approved_at = timezone.now()
        merchant.save()
        return Response({'status': 'Merchant approved'}, status=status.HTTP_200_OK)