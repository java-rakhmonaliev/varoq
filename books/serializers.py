from rest_framework import serializers
from .models import Author, Book, BookAuthor


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookAuthorSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = BookAuthor
        fields = ['id', 'author']


class BookSerializer(serializers.ModelSerializer):
    authors = BookAuthorSerializer(source='book_authors', many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'isbn', 'title', 'description', 'cover_url',
            'published_year', 'page_count', 'language', 'publisher',
            'source', 'is_verified', 'authors', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_verified']