from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from jwt.algorithms import get_default_algorithms

import jwt
import json
import urllib3

from .models import User_Base


class IdentityTokenAuthentication(BaseAuthentication):
    """
    It uses to validate token which generated by identity server
    """
    request = None
    jwt_auth = json.loads(json.dumps(getattr(settings, 'JWT_AUTH', None)))

    def authenticate(self, request):
        self.request = request
        username, message = self.get_user_name_from_token()
        if username == '':
            raise exceptions.AuthenticationFailed(_(message))
        try:
            user = User_Base.objects.get(username__iexact=username)
            auth_user = User()
            auth_user.is_active = True
            auth_user.username = user.username
            if not auth_user.is_active:
                raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
            return auth_user, None
        except User_Base.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

    def authenticate_header(self, request):
        pass

    def get_user_name_from_token(self):
        token = self.get_authorization_token()
        if token:
            try:
                http = urllib3.PoolManager()
                response = http.request('GET', self.jwt_auth['JWKS_URL'])
                jwks = json.dumps(json.loads(response.data.decode('utf-8'))['keys'][0])
                rsa = get_default_algorithms()['RS256']
                cert = rsa.from_jwk(jwks)
                result = jwt.decode(token, cert, options={'verify_aud': False}, algorithms=['RS256'])
                return result['sub'], ''
            except urllib3.exceptions.HTTPError:
                return '', 'Open JWKS Url failed.'
            except jwt.DecodeError:
                return '', 'Signature Decode Failed.'
            except jwt.ExpiredSignature:
                return '', 'Expired Signature.'
        return '', 'Invalid header. No credentials provided.'

    def get_authorization_token(self):
        auth = get_authorization_header(self.request).decode(HTTP_HEADER_ENCODING).split()
        if self.jwt_auth and len(auth) == 2:
            return auth[1] if auth[0].lower() == self.jwt_auth['JWT_AUTH_HEADER_PREFIX'].lower() else None

        return None


class JSONWebTokenAuthentication(BaseAuthentication):
    """
    It uses to validate token which generated by current project
    Header should contain Authorization: Basic XXXXXXXX
    """
    def authenticate(self, request):
        auth = get_authorization_header(request).decode(HTTP_HEADER_ENCODING).split()
        if len(auth) == 2 and auth[0].lower() == 'basic':
            try:
                payload = jwt.decode(auth[1], settings.SECRET_KEY)
                username = payload['username']
                user = User_Base.objects.get(username__iexact=username)
                auth_user = User()
                auth_user.is_active = True
                auth_user.username = user.username
                if not auth_user.is_active:
                    raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

                return auth_user, None
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed(_('Expired Signature.'))
            except jwt.DecodeError:
                raise exceptions.AuthenticationFailed(_('Signature Decode Failed.'))
            except User_Base.DoesNotExist:
                raise exceptions.AuthenticationFailed(_('Invalid username/password.'))
        return None
