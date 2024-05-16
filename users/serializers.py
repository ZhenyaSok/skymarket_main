from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    """
    Регистрация пользователя. (Модель User)
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'phone', 'last_name', 'is_active', 'email', 'password']


class CurrentUserSerializer(serializers.ModelSerializer):
    """Отображение данных пользователя. (Модель User)"""
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']