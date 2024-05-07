# serializers.py
from rest_framework import serializers
from .models import BackupUser, BackupRepository

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupUser
        fields = '__all__'

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupRepository
        fields = '__all__'