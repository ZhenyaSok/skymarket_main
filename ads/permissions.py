from rest_framework.permissions import BasePermission
from users import models

class IsAdminOrOwner(BasePermission):
    message = "Вы не являетесь владельцем или администратором"

    def has_permission(self, request, view):
        """Проверка на аутентификацию"""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверка на владельца или админа"""
        if request.user.role == models.UserRoles.ADMIN:
            return True
        return obj.author == request.user
