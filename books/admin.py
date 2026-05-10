from django.contrib import admin

from .models import Author, Book, BookAuthor


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "isbn",
        "language",
        "published_year",
        "source",
        "is_verified",
        "added_by",
    )
    list_filter = ("source", "language", "is_verified", "published_year")
    search_fields = ("title", "isbn")
    ordering = ("-created_at",)


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ("book", "author")
    raw_id_fields = ("book", "author")
