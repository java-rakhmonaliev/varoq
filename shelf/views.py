from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import UserBook
from .serializers import UserBookSerializer
from books.models import Book


class UserBookViewSet(viewsets.ModelViewSet):
    serializer_class = UserBookSerializer

    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='add-by-isbn')
    def add_by_isbn(self, request):
        """Barcode / ISBN scan endpoint"""
        isbn = request.data.get('isbn')
        if not isbn:
            return Response({"error": "ISBN is required"}, status=400)

        book = Book.objects.filter(isbn=isbn).first()
        if not book:
            return Response({"error": "Book not found"}, status=404)

        user_book, created = UserBook.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'status': 'reading', 'current_page': 0}
        )

        serializer = self.get_serializer(user_book)
        return Response({
            "message": "Book added to shelf",
            "created": created,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def update_progress(self, request, pk=None):
        user_book = self.get_object()
        current_page = request.data.get('current_page')

        if current_page is not None:
            user_book.current_page = current_page
            if current_page >= (user_book.book.page_count or 9999):
                user_book.status = 'finished'
                user_book.finished_at = timezone.now()
            user_book.save()
            serializer = self.get_serializer(user_book)
            return Response(serializer.data)

        return Response({"error": "current_page is required"}, status=400)