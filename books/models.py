from django.db import models
from django.conf import settings


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "authors"
        verbose_name = "Author"
        verbose_name_plural = "Authors"

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
    genre = models.CharField(max_length=100, blank=True)  # e.g. "novel", "fiction", "self-help"
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
            models.Index(fields=["language"]),
            models.Index(fields=["genre"]),
        ]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_authors")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_books")

    class Meta:
        db_table = "book_authors"
        unique_together = ("book", "author")
        verbose_name = "Book Author"
        verbose_name_plural = "Book Authors"

    def __str__(self):
        return f"{self.book.title} — {self.author.name}"