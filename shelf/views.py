from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

from .serializers import UserBookSerializer


from .models import UserBook, ReadingSession
from books.models import Book, Author, BookAuthor          # ← ADD THIS LINE
from books.services.openlibrary import OpenLibraryService

class UserBookViewSet(viewsets.ModelViewSet):
    serializer_class = UserBookSerializer

    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='add-by-isbn')
    def add_by_isbn(self, request):
        """Main barcode/ISBN endpoint - uses Open Library API"""
        isbn = request.data.get('isbn')
        if not isbn:
            return Response({"error": "ISBN is required"}, status=400)

        # 1. Try Open Library API first
        ol_data = OpenLibraryService.get_book_by_isbn(isbn)

        if ol_data:
            # Create or get book from API data
            book, _ = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': ol_data['title'],
                    'description': ol_data.get('description', ''),
                    'cover_url': ol_data.get('cover_url'),
                    'page_count': ol_data.get('page_count'),
                    'published_year': ol_data.get('published_year'),
                    'language': ol_data.get('language', 'en'),
                    'source': 'open_library',
                    'is_verified': True,
                }
            )

            # Link authors
            for author_name in ol_data.get('authors', []):
                author, _ = Author.objects.get_or_create(name=author_name)
                BookAuthor.objects.get_or_create(book=book, author=author)
        else:
            # Fallback: use existing book or require manual entry
            book = Book.objects.filter(isbn=isbn).first()
            if not book:
                return Response({
                    "error": "Book not found in Open Library. Please add manually.",
                    "suggestion": "Use manual book entry for rare/local books"
                }, status=404)

        # Add to user's shelf
        user_book, created = UserBook.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'status': 'reading', 'current_page': 0}
        )

        serializer = self.get_serializer(user_book)
        return Response({
            "message": "Book added to shelf",
            "created": created,
            "from_open_library": bool(ol_data),
            "data": serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    @action(detail=True, methods=['patch'])
    def update_progress(self, request, pk=None):
        user_book = self.get_object()
        new_page = request.data.get('current_page')

        if new_page is None:
            return Response({"error": "current_page is required"}, status=400)

        pages_read = max(0, int(new_page) - user_book.current_page)
        user_book.current_page = new_page

        if new_page >= (user_book.book.page_count or 9999):
            user_book.status = 'finished'
            user_book.finished_at = timezone.now()

        user_book.save()

        # Bug 3 fix — log the session
        if pages_read > 0:
            ReadingSession.objects.create(
                user_book=user_book,
                pages_read=pages_read,
                page_after=new_page,
            )

        return Response(self.get_serializer(user_book).data)