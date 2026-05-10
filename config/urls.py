from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        "status": "healthy",
        "message": "Varoq API is running 🚀"
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health check
    path('api/health/', health_check, name='health-check'),
    
    # App URLs
    path('api/accounts/', include('accounts.urls')),
    path('api/books/', include('books.urls')),
    path('api/shelf/', include('shelf.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/social/', include('social.urls')),
    path('api/feed/', include('feed.urls')),
]