from django.conf import settings
from django.db import models


class Friendship(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("blocked", "Blocked"),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendships_initiated",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendships_received",
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "friendships"
        unique_together = ("requester", "receiver")
        indexes = [
            models.Index(fields=["requester", "status"]),
            models.Index(fields=["receiver", "status"]),
        ]

    def __str__(self):
        return f"{self.requester.phone} → {self.receiver.phone} ({self.status})"
