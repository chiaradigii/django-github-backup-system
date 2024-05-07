# views.py
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .models import BackupUser, BackupRepository
from .serializers import UserSerializer, RepositorySerializer
from .github import get_github_user, get_user_repositories
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def fetch_user(request, username):
    """ Endpoint to fetch user information and display it in the API """
    user = get_object_or_404(BackupUser, username=username) # fetch user from db
    user_data = get_github_user(username) # Fetch user data from GitHub
    if user_data:
        # Fetch repositories linked to the user
        repositories = BackupRepository.objects.filter(user=user) 
        repositories_data = [repo.repository_name for repo in repositories] 

        return Response({
            'status': 'success',
            'data': {
                'user': user_data,
                'repositories': repositories_data,
            }
        })
    else:
        return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def backup_user(request, username):
    """ Endpoint to backup a user to the DB """
    if not BackupUser.objects.filter(username=username).exists():
        user_data = get_github_user(username)
        if user_data:
            user = BackupUser(username=username, github_url=user_data['html_url'])
            user.save()
            return Response({'status': 'success', 'message': 'User backed up'})
        else:
            return Response({'status': 'error', 'message': 'GitHub user not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'status': 'error', 'message': 'User already backed up'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_user(request, username):
    """ Deelete user backup from DB, along with the linked repositories """
    try:
        user = BackupUser.objects.get(username=username)
        user.repositories.all().delete() # Delete associated repositories
        user.delete() # Delete user
        return Response({'status': 'success', 'message': 'User and associated repositories deleted successfully.'})
    except BackupUser.DoesNotExist:
        return Response({'status': 'error', 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND) 

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
        return Response({'status': 'error', 'message': 'User not backed up yet.'}, status=status.HTTP_404_NOT_FOUND)

    user_repositories = get_user_repositories(username)
    repo_name = repository_url.strip('/').split('/')[-1]

    if not any(repo['name'] == repo_name for repo in user_repositories):
        return Response({'status': 'error', 'message': 'The user is not the owner of the repository'}, status=status.HTTP_404_NOT_FOUND)

    if BackupRepository.objects.filter(github_repository_url=repository_url).exists():
        return Response({'status': 'error', 'message': 'The repository is already backed up.'}, status=status.HTTP_404_NOT_FOUND)

    backup_repo = BackupRepository(
        user=user,
        github_repository_url=repository_url,
        repository_name=repo_name
    )
    backup_repo.save()

    return Response({'status': 'success', 'message': 'Repository backed up successfully.'})

@api_view(['DELETE'])
def delete_repository(request, repository_url):
    """ Delete a repo backup from the DB"""
    try:
        repository = BackupRepository.objects.get(github_repository_url=repository_url)
    except BackupRepository.DoesNotExist:
        return Response({'status': 'error', 'message': 'Repository not found.'}, status=status.HTTP_404_NOT_FOUND)

    repository.delete()
    return Response({'status': 'success', 'message': 'Repository deleted successfully.'})

class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows users to be viewed."""
    queryset = BackupUser.objects.all()
    serializer_class = UserSerializer

    def retrieve (self, request, pk=None):
        user_data = get_github_user(pk)
        if user_data:
            # Save data to database
            return Response({'status': 'success', 'data': user_data})
        else:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class RepositoryViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows repositories to be viewed"""
    queryset = BackupRepository.objects.all()
    serializer_class = RepositorySerializer
