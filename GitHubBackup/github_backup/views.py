# views.py
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import BackupUser, BackupRepository
from .serializers import UserSerializer, RepositorySerializer
from .github import get_github_user, get_user_repositories
from rest_framework.decorators import api_view

@api_view(['GET'])
def fetch_user(request, username):
    """ Endpoint to fetch user information and display it in the API """
    user = get_object_or_404(BackupUser, username=username) # fetch user from db
    user_data = get_github_user(username) # Fetch user data from GitHub
    if user_data:
        # Fetch repositories linked to the user
        repositories = BackupRepository.objects.filter(user=user) 
        repositories_data = [repo.repository_name for repo in repositories] 

        return JsonResponse({
            'status': 'success',
            'data': {
                'user': user_data,
                'repositories': repositories_data,
            }
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

@api_view(['POST'])
def backup_user(request, username):
    """ Endpoint to backup a user to the DB """
    if not BackupUser.objects.filter(username=username).exists():
        user_data = get_github_user(username)
        if user_data:
            user = BackupUser(username=username, github_url=user_data['html_url'])
            user.save()
            return JsonResponse({'status': 'success', 'message': 'User backed up'})
        else:
            return JsonResponse({'status': 'error', 'message': 'GitHub user not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'User already backed up'}, status=400)

@api_view(['DELETE'])
def delete_user(username):
    """ Deelete user backup from DB, along with the linked repositories """
    try:
        user = BackupUser.objects.get(username=username)
        user.repositories.all().delete() # Delete associated repositories
        user.delete() # Delete user
        return JsonResponse({'status': 'success', 'message': 'User and associated repositories deleted successfully.'})
    except BackupUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404) 

@api_view(['POST'])
def backup_repository(request, username, repository_url):
    """ Endpoint to backup a repository to the DB 
        - Fetch user and repo from DB if exists
        - Verify ownership of the repo
        - Save repo to DB
    """
    try:
        user = BackupUser.objects.get(username=username)
    except BackupUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not backed up yet.'}, status=404)

    user_repositories = get_user_repositories(username)
    repo_name = repository_url.strip('/').split('/')[-1]

    if not any(repo['name'] == repo_name for repo in user_repositories):
        return JsonResponse({'status': 'error', 'message': 'The user is not the owner of the repository'}, status=400)

    if BackupRepository.objects.filter(github_repository_url=repository_url).exists():
        return JsonResponse({'status': 'error', 'message': 'The repository is already backed up.'}, status=400)

    backup_repo = BackupRepository(
        user=user,
        github_repository_url=repository_url,
        repository_name=repo_name
    )
    backup_repo.save()

    return JsonResponse({'status': 'success', 'message': 'Repository backed up successfully.'})

@api_view(['DELETE'])
def delete_repository(request, repository_url):
    """ Delete a repo backup from the DB"""
    try:
        repository = BackupRepository.objects.get(github_repository_url=repository_url)
    except BackupRepository.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Repository not found.'}, status=404)

    repository.delete()
    return JsonResponse({'status': 'success', 'message': 'Repository deleted successfully.'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = BackupUser.objects.all()
    serializer_class = UserSerializer

    def retrieve (self, request, pk=None):
        user_data = get_github_user(pk)
        if user_data:
            # Save data to database
            return JsonResponse({'status': 'success', 'data': user_data})
        else:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        
class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = BackupRepository.objects.all()
    serializer_class = RepositorySerializer
