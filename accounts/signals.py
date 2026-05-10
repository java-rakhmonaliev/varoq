from django.db.models.signals import post_save
from django.dispatch import receiver
from shelf.models import UserBook
from reviews.models import Review
from feed.models import FeedEvent

STATUS_EVENT_MAP = {
    'reading': 'started_reading',
    'finished': 'finished_book',
}

@receiver(post_save, sender=UserBook)
def create_userbook_event(sender, instance, created, **kwargs):
    if created:
        event_type = 'added_book'
    else:
        event_type = STATUS_EVENT_MAP.get(instance.status)
        if not event_type:
            return  # progress updates, paused, etc. — no event

    FeedEvent.objects.create(
        actor=instance.user,
        event_type=event_type,
        book=instance.book,
        user_book=instance,
    )


@receiver(post_save, sender=Review)
def create_review_event(sender, instance, created, **kwargs):
    if created:
        FeedEvent.objects.create(
            actor=instance.user,
            event_type='wrote_review',
            book=instance.book,
            review=instance,
        )