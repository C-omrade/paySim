from user.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from customer.models import Customer
from merchant.models import Merchant
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], trim_whitespace=False)
    account_type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('merchant', 'Merchant')], required=True)
    business_name = serializers.CharField(required=False, allow_blank=True)
    business_address = serializers.CharField(required=False, allow_blank=True)
    business_email = serializers.EmailField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, attrs):
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        if attrs['account_type'] == 'merchant':
            if not attrs.get('business_name'):
                raise serializers.ValidationError({"business_name": "This field is required for merchants."})
            if not attrs.get('business_address'):
                raise serializers.ValidationError({"business_address": "This field is required for merchants."})
            if not attrs.get('business_email'):
                raise serializers.ValidationError({"business_email": "This field is required for merchants."})

        return attrs 

    class Meta:
        model = User
        fields = ('username', 'name', 'password', 'email', 'first_name', 'last_name', 'account_type', 'business_name', 'business_address', 'business_email')

    @transaction.atomic
    def create(self, validated_data):
        account_type = validated_data.pop('account_type')
        business_name = validated_data.pop('business_name', None)
        business_address = validated_data.pop('business_address', None)
        business_email = validated_data.pop('business_email', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        if account_type == 'customer':
            Customer.objects.create(user=user)
        elif account_type == 'merchant':
            Merchant.objects.create(
                user=user,
                business_name=business_name,
                business_address=business_address,
                business_email=business_email
            )
        return user

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'account_type': 'customer' if hasattr(instance, 'customer_profile') else 'merchant',
        }