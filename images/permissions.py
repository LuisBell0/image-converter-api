from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to perform actions on it.
    Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
