from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Customer
from .serializers import CustomerSerializer


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.select_related("user").all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]