from rest_framework.permissions import BasePermission

class AdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_staff or request.user.is_superuser
