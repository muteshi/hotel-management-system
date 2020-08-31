from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'You have insufficient permissions'

    def has_object_permission(self, request, view, obj):
        return obj.contact_person == request.user


class IsAdmin(BasePermission):
    """Allow access only to admins"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsOwner(BasePermission):
    """Allow access only to owners"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsAdminOrOwner(BasePermission):
    """Allow access to admins and owners"""  
    def has_object_permission(*args):
        return (IsAdmin.has_object_permission(*args) or
                IsOwner.has_object_permission(*args))





