from rest_framework import viewsets, permissions
from .models import Friendship
from .serializers import FriendshipSerializer, FriendshipCreateSerializer


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.select_related('requester', 'receiver').all()
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return FriendshipCreateSerializer
        return FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            models.Q(requester=user) | models.Q(receiver=user)
        )