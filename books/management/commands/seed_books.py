from django.core.management.base import BaseCommand
from books.models import Author, Book, BookAuthor


class Command(BaseCommand):
    help = 'Seed initial Uzbek and international books for Varoq'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding books...')

        # === Authors ===
        a1 = Author.objects.get_or_create(name="Abdulla Qodiriy")[0]
        a2 = Author.objects.get_or_create(name="O'tkir Hoshimov")[0]
        a3 = Author.objects.get_or_create(name="J.K. Rowling")[0]
        a4 = Author.objects.get_or_create(name="George Orwell")[0]

        # === Books + Link Authors ===
        book1, _ = Book.objects.get_or_create(
            isbn="9789943367890",
            defaults={
                'title': "O'tgan Kunlar",
                'description': "O'zbekistonning klassik romani",
                'language': 'uz',
                'page_count': 320,
                'source': 'seed',
                'is_verified': True,
            }
        )
        BookAuthor.objects.get_or_create(book=book1, author=a1)

        book2, _ = Book.objects.get_or_create(
            isbn="9789943367906",
            defaults={
                'title': "Dunyoning Ishlari",
                'description': "O'tkir Hoshimovning mashhur asari",
                'language': 'uz',
                'page_count': 280,
                'source': 'seed',
                'is_verified': True,
            }
        )
        BookAuthor.objects.get_or_create(book=book2, author=a2)

        book3, _ = Book.objects.get_or_create(
            isbn="9781408855652",
            defaults={
                'title': "Harry Potter and the Philosopher's Stone",
                'description': "The boy who lived...",
                'language': 'en',
                'page_count': 223,
                'source': 'seed',
                'is_verified': True,
            }
        )
        BookAuthor.objects.get_or_create(book=book3, author=a3)

        book4, _ = Book.objects.get_or_create(
            isbn="9780451524935",
            defaults={
                'title': "1984",
                'description': "Big Brother is watching you",
                'language': 'en',
                'page_count': 328,
                'source': 'seed',
                'is_verified': True,
            }
        )
        BookAuthor.objects.get_or_create(book=book4, author=a4)

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully seeded {Book.objects.count()} books!'))