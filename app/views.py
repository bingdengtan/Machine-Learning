from rest_framework import viewsets, permissions, renderers
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.response import Response
from rest_framework import serializers, exceptions
from django.http import JsonResponse
from django.conf import settings
from django.utils.translation import ugettext as _
from rest_framework_jwt.settings import api_settings
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime
import jwt
from django.contrib.auth.hashers import PBKDF2PasswordHasher

from .serializers import UserBaseSerializer
from .models import User_Base
from .permissions import IsAuthenticated

# Create your views here.


class UserBaseViewSet(viewsets.ModelViewSet):
    """
    User base view set
    """
    queryset = User_Base.objects.all()
    serializer_class = UserBaseSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = UserBaseSerializer(data=request.data)
        users = User_Base.objects.filter(
            Q(username__iexact=request.data.get('username')) | Q(email__iexact=request.data.get('email'))
        )
        if len(users) >= 1:
            msg = _('User name or email already exists!')
            raise serializers.ValidationError({'detail': msg})

        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
        else:
            raise serializers.ValidationError(serializer.errors)


class JSONWebTokenObtainViewSet(ObtainJSONWebToken):
    """
    It uses to validate user name and password and will return a token to front end user
    """
    def post(self, request, *args, **kwargs):
        hasher = PBKDF2PasswordHasher()
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            msg = _('Must include "username" and "password".')
            raise exceptions.NotAcceptable(msg)

        try:
            user = User_Base.objects.get(username__iexact=username)
            if not hasher.verify(password, user.password):
                raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

            payload = {
                'username': user.username,
                'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
            }
            token = jwt.encode(payload, settings.SECRET_KEY)

            return Response({'token': token, 'username': user.username})
        except User_Base.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))
