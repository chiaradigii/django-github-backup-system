# models.py
from django.db import models

class BackupUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    github_url = models.URLField()

    def __str__(self):
        return self.username

class BackupRepository(models.Model):
    user = models.ForeignKey(BackupUser, related_name='repositories', on_delete=models.CASCADE)
    github_repository_url = models.URLField()
    repository_name = models.CharField(max_length=255)

    def __str__(self):
        return self.repository_name