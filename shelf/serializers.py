from rest_framework import serializers
from .models import UserBook, ReadingSession


class ReadingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingSession
        fields = ['id', 'pages_read', 'page_after', 'logged_at']
        read_only_fields = ['id', 'logged_at']


class UserBookSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)  # or import BookSerializer if you want full data
    reading_sessions = ReadingSessionSerializer(many=True, read_only=True)

    class Meta:
        model = UserBook
        fields = [
            'id', 'book', 'status', 'current_page',
            'started_at', 'finished_at', 'reading_sessions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']