from rest_framework.permissions import BasePermission

class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_superuser or request.user.is_staff



class IsWriterOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_superuser or
                request.user.is_staff or
                request.user == obj

        )

