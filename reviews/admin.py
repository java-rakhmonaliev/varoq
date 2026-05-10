from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'is_public', 'created_at')
    raw_id_fields = ('user_book',)
    list_filter = ('is_public', 'rating')
    search_fields = (
        'user_book__user__phone',
        'user_book__book__title',
        'body'
    )
    autocomplete_fields = ('user_book',)   # Recommended over raw_id_fields

    def user(self, obj):
        return obj.user_book.user

    user.admin_order_field = 'user_book__user__phone'
    user.short_description = 'User'

    def book(self, obj):
        return obj.user_book.book

    book.admin_order_field = 'user_book__book__title'
    book.short_description = 'Book'