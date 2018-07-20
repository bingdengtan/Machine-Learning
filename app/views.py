from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, renderers
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.response import Response
from rest_framework import serializers, exceptions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework import views

from datetime import datetime
from django.utils import timezone
import jwt
import json
import numpy as np

import app.core.utils as utils
from app.serializers import UserBaseSerializer, RoleBaseSerializer
from app.models import User_Base, Role_Base
from app.permissions import IsAuthenticated
from app.core.utils import encode_password

# Create your views here.
import os
import datetime
import sys
import mongoengine
from keras.models import load_model

class UserBaseViewSet(viewsets.ModelViewSet):
    """
    User base view set
    """
    serializer_class = UserBaseSerializer

    def get_queryset(self):
        queryset = User_Base.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data))
        data['created_by'] = request.user.username
        data['last_updated_by'] = request.user.username
        data['last_updated_date'] = timezone.now()
        data['creation_date'] = timezone.now()

        if utils.has_attribute(data, 'password'):
            data['password'] = encode_password(request.data.get('password'))

        serializer = self.serializer_class(data=data)

        if self.serializer_class().is_user_exist(data):
            msg = _('User name or email already exists!')
            raise serializers.ValidationError({'detail': msg})

        if serializer.is_valid():
            serializer.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
        else:
            raise serializers.ValidationError(serializer.errors)

    def update(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data))
        if self.serializer_class().is_user_exist(data):
            msg = _('User name or email already exists!')
            raise serializers.ValidationError({'detail': msg})

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class
        serializer.Meta.fields = getattr(serializer, 'list_fields', None) or serializer.Meta.fields
        if request.query_params.get('ordering', None):
            queryset = self.filter_queryset(self.get_queryset().order_by(request.GET['ordering']))
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RoleBaseViewSet(viewsets.ModelViewSet):
    serializer_class = RoleBaseSerializer

    def get_queryset(self):
        queryset = Role_Base.objects.all()
        role_name = self.request.query_params.get('role_name', None)
        if role_name is not None:
            queryset = queryset.filter(role_name__icontains=role_name)
        return queryset

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data))

        data['created_by'] = 'BingDeng Tan'
        data['last_updated_by'] = 'BingDeng Tan'
        data['last_updated_date'] = timezone.now()
        data['creation_date'] = timezone.now()

        serializer = self.serializer_class(data=data)
        if self.serializer_class().is_role_exist(data):
            msg = _('Role name already exists!')
            raise serializers.ValidationError({'detail': msg})

        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
        else:
            raise serializers.ValidationError(serializer.errors)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if self.serializer_class().is_role_exist(request.data):
            msg = _('Role name already exists!')
            raise serializers.ValidationError({'detail': msg})

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class
        serializer.Meta.fields = getattr(serializer, 'list_fields', None) or serializer.Meta.fields
        if request.query_params.get('ordering', None):
            queryset = self.filter_queryset(self.get_queryset().order_by(request.GET['ordering']))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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


class MLViewSet(views.APIView):
    def post(self, request, *args, **kwargs):
        import numpy as np
        model = settings.ML_MODEL
        X = np.array([[0.7,1.,1.,1.,0.,1.,0.,1.,0.8]])
        prediction = model.predict(X)
        aa = prediction
        print(prediction)
        prediction = prediction + 0.1159
        prediction = prediction / 0.0000036968
        print("Earnings Prediction for Proposed Product - ${}".format(prediction))
        return Response({'prediction': aa, 'result': prediction[0][0]})