from django.contrib import admin

from .models import FeedEvent, Reaction


@admin.register(FeedEvent)
class FeedEventAdmin(admin.ModelAdmin):
    list_display = ("actor", "event_type", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("actor__phone", "actor__display_name")
    raw_id_fields = ("actor", "book", "user_book", "review")
    ordering = ("-created_at",)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "reaction_type", "created_at")
    list_filter = ("reaction_type", "created_at")
    search_fields = ("user__phone", "event__actor__phone")
    raw_id_fields = ("user", "event")
    ordering = ("-created_at",)
