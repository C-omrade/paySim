import random

from rest_framework import serializers

from customer.models import Customer
from merchant.models import Merchant
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "transaction_id",
            "merchant",
            "customer",
            "amount",
            "currency",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "transaction_id",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )
        return value

    def validate_merchant(self, value):
        if value.status != "approved":
            raise serializers.ValidationError(
                "Only approved merchants can accept payments."
            )
        return value

    def validate_customer(self, value):
        return value

    def create(self, validated_data):
        # Simulate a payment processor response.
        validated_data["status"] = random.choices(
            ["SUCCESS", "FAILED"],
            weights=[90, 10],
            k=1,
        )[0]

        return Payment.objects.create(**validated_data)