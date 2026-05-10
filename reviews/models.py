from django.conf import settings
from django.db import models


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    body = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"
        unique_together = ("user", "book")  # one review per user per book
        indexes = [
            models.Index(fields=["book", "is_public"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.phone} — {self.book.title} ({self.rating}★)"
