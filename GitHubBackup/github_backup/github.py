# GitHub API functions github.py
import requests
from django.conf import settings

def get_github_user(username):
    """Fetch a user's profile from GitHub."""
    url = f"https://api.github.com/users/{username}"
    headers = {'Authorization': f'token {settings.GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_user_repositories(username):
    """Fetch a list of repositories for a given GitHub user."""
    url = f"https://api.github.com/users/{username}/repos"
    headers = {'Authorization': f'token {settings.GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
