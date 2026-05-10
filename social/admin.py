from django.contrib import admin

from .models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ("requester", "receiver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = (
        "requester__phone",
        "requester__display_name",
        "receiver__phone",
        "receiver__display_name",
    )
    raw_id_fields = ("requester", "receiver")
    ordering = ("-created_at",)
