from rest_framework import serializers
from .models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    requester = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Friendship
        fields = [
            'id', 'requester', 'receiver', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FriendshipCreateSerializer(serializers.ModelSerializer):
    """Used when sending friend request"""
    class Meta:
        model = Friendship
        fields = ['receiver']