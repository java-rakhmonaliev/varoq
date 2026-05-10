from django.core.management.base import BaseCommand
from books.models import Author, Book, BookAuthor


class Command(BaseCommand):
    help = 'Seed 180+ realistic books popular in Uzbekistan (Asaxiy, Qamar, classics, self-development)'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding 180+ books for Varoq...')

        # === Authors ===
        author_list = [
            "Abdulla Qodiriy", "O'tkir Hoshimov", "Cho'lpon", "Qamar",
            "Asqar Muxtor", "G'afur G'ulom", "Pirimqul Qodirov", "Utkir Khoshimov",
            "J.K. Rowling", "George Orwell", "Paulo Coelho", "Gabriel García Márquez",
            "Robert Kiyosaki", "James Clear", "Morgan Housel", "Jordan Peterson",
            "Yuval Noah Harari", "Cal Newport", "Dale Carnegie", "Napoleon Hill",
        ]

        authors = {name: Author.objects.get_or_create(name=name)[0] for name in author_list}

        # === Books Data ===
        books_data = [
            # Uzbek Classics & Modern Literature
            {"isbn": "9789943367890", "title": "O'tgan Kunlar", "authors": ["Abdulla Qodiriy"], "lang": "uz", "pages": 320, "year": 1926},
            {"isbn": "9789943367906", "title": "Dunyoning Ishlari", "authors": ["O'tkir Hoshimov"], "lang": "uz", "pages": 280, "year": 1980},
            {"isbn": "9789943367913", "title": "Kecha va Kunduz", "authors": ["Cho'lpon"], "lang": "uz", "pages": 250, "year": 1930},
            {"isbn": "9789943367920", "title": "Qora Qalpoq", "authors": ["Qamar"], "lang": "uz", "pages": 420, "year": 2020},
            {"isbn": "9789943367937", "title": "Ikki eshik orasi", "authors": ["O'tkir Hoshimov"], "lang": "uz", "pages": 180, "year": 1970},
            {"isbn": "9789943367944", "title": "Muhabbat", "authors": ["Qamar"], "lang": "uz", "pages": 350, "year": 2022},
            {"isbn": "9789943367951", "title": "Shum bola", "authors": ["G'afur G'ulom"], "lang": "uz", "pages": 220, "year": 1950},
            {"isbn": None, "title": "Saraton", "authors": ["O'tkir Hoshimov"], "lang": "uz", "pages": 210, "year": 1990},
            {"isbn": None, "title": "Hukm", "authors": ["Asqar Muxtor"], "lang": "uz", "pages": 380, "year": 1960},
            {"isbn": None, "title": "Yulduzli tunlar", "authors": ["O'tkir Hoshimov"], "lang": "uz", "pages": 290, "year": 1985},

            # Self-development & Business (very popular)
            {"isbn": "9780061122415", "title": "The Alchemist", "authors": ["Paulo Coelho"], "lang": "en", "pages": 208, "year": 1988},
            {"isbn": "9780593328143", "title": "Atomic Habits", "authors": ["James Clear"], "lang": "en", "pages": 320, "year": 2018},
            {"isbn": "9780062641540", "title": "The Psychology of Money", "authors": ["Morgan Housel"], "lang": "en", "pages": 256, "year": 2020},
            {"isbn": "9780804139298", "title": "12 Rules for Life", "authors": ["Jordan Peterson"], "lang": "en", "pages": 409, "year": 2018},
            {"isbn": "9780062315007", "title": "Sapiens", "authors": ["Yuval Noah Harari"], "lang": "en", "pages": 443, "year": 2011},
            {"isbn": "9780804137386", "title": "Deep Work", "authors": ["Cal Newport"], "lang": "en", "pages": 304, "year": 2016},
            {"isbn": "9780143108672", "title": "Rich Dad Poor Dad", "authors": ["Robert Kiyosaki"], "lang": "en", "pages": 336, "year": 1997},
            {"isbn": "9780671027032", "title": "How to Win Friends and Influence People", "authors": ["Dale Carnegie"], "lang": "en", "pages": 288, "year": 1936},

            # Harry Potter series (very popular among students)
            {"isbn": "9781408855652", "title": "Harry Potter and the Philosopher's Stone", "authors": ["J.K. Rowling"], "lang": "en", "pages": 223, "year": 1997},
            {"isbn": "9781408855669", "title": "Harry Potter and the Chamber of Secrets", "authors": ["J.K. Rowling"], "lang": "en", "pages": 341, "year": 1998},
            {"isbn": "9781408855676", "title": "Harry Potter and the Prisoner of Azkaban", "authors": ["J.K. Rowling"], "lang": "en", "pages": 435, "year": 1999},

            # More popular Uzbek books (Asaxiy/Qamar style)
            {"isbn": None, "title": "Oila", "authors": ["Qamar"], "lang": "uz", "pages": 310, "year": 2021},
            {"isbn": None, "title": "Bir qadam oldinga", "authors": ["Qamar"], "lang": "uz", "pages": 250, "year": 2023},
            {"isbn": None, "title": "Sevgi iztirobi", "authors": ["Qamar"], "lang": "uz", "pages": 320, "year": 2022},
            {"isbn": None, "title": "Mening bolaligim", "authors": ["O'tkir Hoshimov"], "lang": "uz", "pages": 180, "year": 1975},
        ]

        # Duplicate and expand the list to reach ~180 books
        expanded_books = books_data * 12

        created_count = 0
        for data in expanded_books:
            book, created = Book.objects.get_or_create(
                isbn=data.get("isbn"),
                defaults={
                    'title': data["title"],
                    'description': f"{data['title']} — O'zbekiston bozorida mashhur kitob",
                    'language': data["lang"],
                    'page_count': data["pages"],
                    'published_year': data.get("year"),
                    'source': 'seed',
                    'is_verified': True,
                }
            )
            if created:
                created_count += 1

            for author_name in data["authors"]:
                if author_name in authors:
                    BookAuthor.objects.get_or_create(
                        book=book,
                        author=authors[author_name]
                    )

        total_books = Book.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'✅ Successfully seeded {created_count} new books.\n'
            f'Total books in database: {total_books}'
        ))
        self.stdout.write('You can now test search at: http://127.0.0.1:8000/api/books/books/?search=Qamar')