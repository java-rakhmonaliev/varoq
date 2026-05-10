import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    phone = PhoneNumberField(unique=True, region="UZ")
    display_name = models.CharField(max_length=150, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)
    annual_reading_goal = models.PositiveSmallIntegerField(default=12)

    username = None
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["display_name"]

    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return str(self.phone)


class OTPCode(models.Model):
    phone = PhoneNumberField(region="UZ")
    code = models.CharField(max_length=6)
    session_token = models.UUIDField(default=uuid.uuid4, unique=True)  # deep link token
    chat_id = models.BigIntegerField(null=True, blank=True)             # set by bot on /start
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otp_codes"

    def __str__(self):
        return f"{self.phone} - {self.code}"