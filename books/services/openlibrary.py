import requests
from django.conf import settings


class OpenLibraryService:
    BASE_URL = "https://openlibrary.org/api/books"

    @staticmethod
    def get_book_by_isbn(isbn: str):
        """
        Fetch book data from Open Library by ISBN.
        Returns dict with book data or None if not found.
        """
        if not isbn:
            return None

        url = f"{OpenLibraryService.BASE_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        
        try:
            response = requests.get(url, timeout=8)
            response.raise_for_status()
            data = response.json()

            if not data:
                return None

            key = f"ISBN:{isbn}"
            if key not in data:
                return None

            book_data = data[key]

            # Extract useful fields
            title = book_data.get('title')
            if not title:
                return None

            authors = []
            if 'authors' in book_data:
                authors = [author.get('name') for author in book_data.get('authors', []) if author.get('name')]

            cover_url = None
            if 'cover' in book_data and book_data['cover'].get('large'):
                cover_url = book_data['cover']['large']
            elif book_data.get('cover_url'):
                cover_url = book_data.get('cover_url')

            return {
                'isbn': isbn,
                'title': title,
                'description': book_data.get('description', ''),
                'cover_url': cover_url,
                'page_count': book_data.get('number_of_pages'),
                'published_year': book_data.get('publish_date'),
                'authors': authors,
                'language': book_data.get('languages', [{}])[0].get('key', '/languages/eng').split('/')[-1] if book_data.get('languages') else 'en',
            }
        except Exception as e:
            print(f"Open Library API error: {e}")
            return None
