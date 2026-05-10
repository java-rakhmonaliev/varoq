from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import User, OTPCode


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'display_name', 'avatar_url', 'bio', 'annual_reading_goal', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Used for user creation (kept for future use)"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'display_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            display_name=validated_data.get('display_name', '')
        )
        return user


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

    def validate_phone(self, value):
        if not value.startswith('+998'):
            raise serializers.ValidationError("Phone must start with +998")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)