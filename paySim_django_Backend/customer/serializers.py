from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Customer
        fields = [
            "id",
            "user",
            "name",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_name(self, obj):
        return obj.user.name    