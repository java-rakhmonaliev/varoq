from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from .models import User, OTPCode
from .serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer


class AuthViewSet(viewsets.ViewSet):
    permission_classes = []

    @action(detail=False, methods=['post'])
    def send_otp(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            user, _ = User.objects.get_or_create(
                phone=phone,
                defaults={'display_name': 'New Reader'}
            )

            code = "123456"  # TODO: real random + Eskiz.uz later
            OTPCode.objects.create(
                phone=phone,
                code=code,
                expires_at=timezone.now() + timedelta(minutes=5)
            )

            return Response({
                "message": "OTP sent successfully",
                "phone": str(phone),
                "code": code   # remove in production
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']

            otp = OTPCode.objects.filter(
                phone=phone, code=code, used_at__isnull=True,
                expires_at__gt=timezone.now()
            ).first()

            if otp:
                otp.used_at = timezone.now()
                otp.save()

                user = User.objects.get(phone=phone)
                refresh = RefreshToken.for_user(user)

                return Response({
                    "message": "Login successful",
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                })
            return Response({"error": "Invalid or expired OTP"}, status=400)
        return Response(serializer.errors, status=400)