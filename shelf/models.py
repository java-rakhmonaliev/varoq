from django.conf import settings
from django.db import models


class UserBook(models.Model):
    STATUS_CHOICES = [
        ("want_to_read", "Want to Read"),
        ("reading", "Reading"),
        ("finished", "Finished"),
        ("paused", "Paused"),
        ("abandoned", "Abandoned"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shelf"
    )
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="user_books"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="want_to_read"
    )
    current_page = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_books"
        unique_together = ("user", "book")
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["book"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.book.title}"


class ReadingSession(models.Model):
    """Append-only log for every page update (for streaks & analytics in v2)"""

    user_book = models.ForeignKey(
        UserBook, on_delete=models.CASCADE, related_name="reading_sessions"
    )
    pages_read = models.PositiveIntegerField()
    page_after = models.PositiveIntegerField()
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reading_sessions"
        ordering = ["-logged_at"]

    def __str__(self):
        return f"{self.user_book} - {self.pages_read} pages"
