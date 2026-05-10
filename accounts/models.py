from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
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

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    phone = PhoneNumberField(unique=True, region="UZ")
    display_name = models.CharField(max_length=150, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)
    reading_goal_2026 = models.PositiveSmallIntegerField(default=12)

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
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otp_codes"

    def __str__(self):
        return f"{self.phone} - {self.code}"
