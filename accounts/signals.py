from django.db.models.signals import post_save
from django.dispatch import receiver
from shelf.models import UserBook
from reviews.models import Review
from feed.models import FeedEvent


@receiver(post_save, sender=UserBook)
def create_userbook_event(sender, instance, created, **kwargs):
    if created or instance.status in ['finished', 'reading']:
        FeedEvent.objects.create(
            actor=instance.user,
            event_type='added_book' if created else 'updated_progress',
            book=instance.book,
            user_book=instance
        )


@receiver(post_save, sender=Review)
def create_review_event(sender, instance, created, **kwargs):
    if created:
        FeedEvent.objects.create(
            actor=instance.user,
            event_type='wrote_review',
            book=instance.book,
            review=instance
        )