from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'user_book',
            'book',
            'rating',
            'body',
            'is_public',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'book']

    def get_book(self, obj):
        b = obj.user_book.book
        return {
            'id': b.id,
            'title': b.title,
            'cover_url': b.cover_url,
        }