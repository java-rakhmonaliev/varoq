from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserBookViewSet

router = DefaultRouter()
router.register(r'', UserBookViewSet, basename='userbook')

urlpatterns = [
    path('', include(router.urls)),
]