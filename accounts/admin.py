from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import OTPCode, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("phone", "display_name", "is_active", "created_at")
    list_filter = ("is_active", "is_staff")
    search_fields = ("phone", "display_name")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal Info", {"fields": ("display_name", "avatar_url", "bio")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "display_name", "password1", "password2"),
            },
        ),
    )


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "expires_at", "used_at")
    list_filter = ("used_at",)
    search_fields = ("phone",)
