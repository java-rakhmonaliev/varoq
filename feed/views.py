from rest_framework import viewsets
from .models import FeedEvent
from .serializers import FeedEventSerializer


class FeedEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedEventSerializer
    permission_classes = []  # temporary - later restrict to friends

    def get_queryset(self):
        return FeedEvent.objects.select_related('actor', 'book')\
            .prefetch_related('reactions')\
            .order_by('-created_at')[:30]