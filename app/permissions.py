from rest_framework import permissions
from .authentication import JSONWebTokenAuthentication


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_user, message = JSONWebTokenAuthentication().authenticate(request)
        return auth_user is not None and auth_user.Is_Active == 'Y'
