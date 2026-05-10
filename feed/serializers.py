from rest_framework import serializers
from .models import FeedEvent, Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'user', 'reaction_type', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class FeedEventSerializer(serializers.ModelSerializer):
    reactions = ReactionSerializer(many=True, read_only=True)

    class Meta:
        model = FeedEvent
        fields = [
            'id', 'actor', 'event_type', 'book', 'user_book', 'review',
            'reactions', 'created_at'
        ]
        read_only_fields = ['id', 'actor', 'created_at']