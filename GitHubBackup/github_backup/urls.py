# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RepositoryViewSet, backup_user, delete_user, backup_repository, delete_repository

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('repositories', RepositoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('backup_user/<str:username>/', backup_user, name='backup_user'),
    path('delete_user/<str:username>/', delete_user, name='delete_user'),
    path('backup_repository/<str:username>/<path:repository_url>/', backup_repository, name='backup_repository'),
    path('delete_repository/<path:repository_url>/', delete_repository, name='delete_repository'),
]