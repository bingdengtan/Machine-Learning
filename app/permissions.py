from rest_framework import permissions
from .authentication import JSONWebTokenAuthentication


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        # You can defined view permission here
        """
        :param request:
        :param view:
        :return: True / False

        Sample:
            auth_user, message = JSONWebTokenAuthentication().authenticate(request)
            return auth_user is not None and auth_user.is_active

        """
        return True
