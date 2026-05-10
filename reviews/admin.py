from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "rating", "is_public", "created_at")
    list_filter = ("rating", "is_public", "created_at")
    search_fields = ("user__phone", "user__display_name", "book__title", "body")
    raw_id_fields = ("user", "book")
    ordering = ("-created_at",)
