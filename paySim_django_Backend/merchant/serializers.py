from rest_framework import serializers
from .models import Merchant


class MerchantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Merchant
        fields = [
            "id",
            "user",
            "name",
            "business_name",
            "business_email",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def get_name(self, obj):
        return obj.user.name