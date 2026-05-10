from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Review has no direct user FK — must traverse through user_book
        return Review.objects.filter(
            user_book__user=self.request.user
        ).select_related('user_book__book')

    def perform_create(self, serializer):
        user_book = serializer.validated_data.get('user_book')
        # Guard: prevent reviewing someone else's shelf entry
        if user_book.user != self.request.user:
            raise PermissionDenied("You can only review your own shelf entries.")
        serializer.save()