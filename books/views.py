from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('book_authors__author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """Support basic search"""
        queryset = self.get_queryset()
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)
        serializer = self.get_serializer(queryset[:20], many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]