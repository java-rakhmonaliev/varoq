import random
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from decouple import config
from .models import User, OTPCode
from .serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer

BOT_USERNAME = config("TELEGRAM_BOT_USERNAME", default="VaroqBot")


class AuthViewSet(viewsets.ViewSet):
    permission_classes = []

    @action(detail=False, methods=['post'])
    def send_otp(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        phone = serializer.validated_data['phone']
        User.objects.get_or_create(phone=phone, defaults={'display_name': 'New Reader'})

        code = f"{random.randint(100000, 999999)}"
        otp = OTPCode.objects.create(
            phone=phone,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=5),
        )

        bot_url = f"https://t.me/{BOT_USERNAME}?start={otp.session_token}"

        return Response({
            "message": "Open the bot to get your code",
            "bot_url": bot_url,
            "session_token": str(otp.session_token),
        })

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        otp = OTPCode.objects.filter(
            phone=phone, code=code,
            used_at__isnull=True,
            expires_at__gt=timezone.now()
        ).first()

        if not otp:
            return Response({"error": "Invalid or expired OTP"}, status=400)

        otp.used_at = timezone.now()
        otp.save()

        user = User.objects.get(phone=phone)
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user