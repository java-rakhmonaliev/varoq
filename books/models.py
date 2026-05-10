from django.conf import settings
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "authors"

    def __str__(self):
        return self.name


class Book(models.Model):
    SOURCE_CHOICES = [
        ("open_library", "Open Library"),
        ("google_books", "Google Books"),
        ("community", "Community"),
        ("seed", "Seed"),
    ]

    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True, null=True)
    published_year = models.PositiveSmallIntegerField(null=True, blank=True)
    page_count = models.PositiveSmallIntegerField(null=True, blank=True)
    language = models.CharField(max_length=10, default="uz")
    publisher = models.CharField(max_length=255, blank=True)
    source = models.CharField(
        max_length=20, choices=SOURCE_CHOICES, default="community"
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "books"
        indexes = [
            models.Index(fields=["isbn"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    """Junction table for many-to-many between Book and Author"""

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_authors"
    )
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="book_authors"
    )

    class Meta:
        db_table = "book_authors"
        unique_together = ("book", "author")

    def __str__(self):
        return f"{self.book.title} — {self.author.name}"
