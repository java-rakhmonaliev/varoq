from django.db import models as django_models
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import FeedEvent, Reaction
from .serializers import FeedEventSerializer, ReactionSerializer
from social.models import Friendship


class FeedEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = Friendship.objects.filter(
            django_models.Q(requester=user) | django_models.Q(receiver=user),
            status='accepted'
        ).values_list('requester_id', 'receiver_id')

        friend_ids = set()
        for requester_id, receiver_id in friends:
            friend_ids.add(requester_id if requester_id != user.id else receiver_id)
        friend_ids.add(user.id)  # include own events

        return FeedEvent.objects.filter(actor_id__in=friend_ids)\
            .select_related('actor', 'book')\
            .prefetch_related('reactions')\
            .order_by('-created_at')

    @action(detail=True, methods=['post'])
    def react(self, request, pk=None):
        event = self.get_object()
        reaction_type = request.data.get('type', 'reading_too')

        reaction, created = Reaction.objects.get_or_create(
            event=event,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )
        if not created:
            reaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # toggle off

        return Response(ReactionSerializer(reaction).data, status=status.HTTP_201_CREATED)