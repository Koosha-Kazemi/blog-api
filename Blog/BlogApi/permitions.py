from rest_framework.permissions import BasePermission

class AdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_staff or request.user.is_superuser


class IsWriterOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_superuser or
                request.user.is_staff or
                request.user == obj

        )

