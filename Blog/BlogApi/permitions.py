from rest_framework.permissions import BasePermission, SAFE_METHODS
from setuptools.package_index import user_agent


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_superuser or request.user.is_staff and request.user.is_authenticated



class IsWriterOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        elif request.user.is_anonymous:
            return
        return (
            request.user.is_superuser or
                request.user.is_staff or
                request.user.is_writer

        )