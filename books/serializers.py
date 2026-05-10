from rest_framework import serializers
from .models import Book, Author, BookAuthor


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "isbn",
            "title",
            "description",
            "cover_url",
            "published_year",
            "page_count",
            "language",
            "publisher",
            "genre",
            "source",
            "is_verified",
            "created_at",
            "updated_at",
            "authors",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "source", "is_verified"]

    def get_authors(self, obj):
        return [ba.author.name for ba in obj.book_authors.select_related("author").all()]