from django.conf import settings
from django.db import models


class FeedEvent(models.Model):
    EVENT_CHOICES = [
        ("added_book", "Added book to shelf"),
        ("started_reading", "Started reading"),
        ("finished_book", "Finished book"),
        ("updated_progress", "Updated progress"),
        ("wrote_review", "Wrote review"),
    ]

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="generated_events",
    )
    event_type = models.CharField(max_length=30, choices=EVENT_CHOICES)

    # References
    book = models.ForeignKey(
        "books.Book", on_delete=models.SET_NULL, null=True, blank=True
    )
    user_book = models.ForeignKey(
        "shelf.UserBook", on_delete=models.SET_NULL, null=True, blank=True
    )
    review = models.ForeignKey(
        "reviews.Review", on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "feed_events"
        indexes = [
            models.Index(fields=["actor", "created_at"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.actor.phone} - {self.get_event_type_display()}"


class Reaction(models.Model):
    REACTION_CHOICES = [
        ("reading_too", "I'm reading this too"),
        ("liked", "Liked"),
        ("inspired", "Inspired me"),
    ]

    event = models.ForeignKey(
        FeedEvent, on_delete=models.CASCADE, related_name="reactions"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reactions"
    )
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reactions"
        unique_together = ("event", "user")
        indexes = [
            models.Index(fields=["event"]),
        ]

    def __str__(self):
        return f"{self.user.phone} reacted to {self.event}"
