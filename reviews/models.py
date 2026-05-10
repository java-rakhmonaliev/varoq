from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from shelf.models import UserBook


class Review(models.Model):
    user_book = models.ForeignKey(UserBook, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    body = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        # One review per shelf entry (UserBook already guarantees one per user+book)
        constraints = [
            models.UniqueConstraint(
                fields=["user_book"],
                name="unique_review_per_user_book"
            )
        ]
        indexes = [
            models.Index(fields=["is_public"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Review by {self.user_book.user} on {self.user_book.book}"