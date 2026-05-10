from django.db import models
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related("book_authors__author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Free-text search (title or author name)
        search = request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search)
                | models.Q(book_authors__author__name__icontains=search)
            ).distinct()

        # Filters
        language = request.query_params.get("language", None)
        if language:
            queryset = queryset.filter(language__iexact=language)

        author = request.query_params.get("author", None)
        if author:
            queryset = queryset.filter(
                book_authors__author__name__icontains=author
            ).distinct()

        genre = request.query_params.get("genre", None)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)

        # Optional: limit results for performance
        serializer = self.get_serializer(queryset[:100], many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]