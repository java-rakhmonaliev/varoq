from django.contrib import admin

from .models import ReadingSession, UserBook


@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "book",
        "status",
        "current_page",
        "started_at",
        "finished_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__phone", "user__display_name", "book__title")
    raw_id_fields = ("user", "book")
    ordering = ("-created_at",)


@admin.register(ReadingSession)
class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = ("user_book", "pages_read", "page_after", "logged_at")
    list_filter = ("logged_at",)
    raw_id_fields = ("user_book",)
    ordering = ("-logged_at",)
