from django.db import models
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Friendship
from .serializers import FriendshipSerializer, FriendshipCreateSerializer


class FriendshipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return FriendshipCreateSerializer
        return FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.select_related('requester', 'receiver').filter(
            models.Q(requester=user) | models.Q(receiver=user)
        )

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        if friendship.status != 'pending':
            return Response({"error": "Already responded"}, status=400)
        friendship.status = 'accepted'
        friendship.save()
        return Response(FriendshipSerializer(friendship).data)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)