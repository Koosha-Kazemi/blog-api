from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
       if request.method == "GET":
           if request.user.is_authenticated:
               return request.user.is_superuser or request.user.is_staff



class IsWriterOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        elif request.user.is_anonymous:
            return False
        return (
            request.user.is_superuser or
                request.user.is_staff or
                request.user.is_writer

        )