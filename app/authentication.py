from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.conf import settings
from jwt.algorithms import get_default_algorithms
from urllib import request
from urllib.error import HTTPError
import jwt
import json
import chilkat

from .models import User_Base


class JSONWebTokenAuthentication(BaseAuthentication):
    request = None
    jwt_auth = json.loads(json.dumps(getattr(settings, 'JWT_AUTH', None)))

    def authenticate(self, request):
        self.request = request
        username, message = self.get_user_name_from_token()
        if username == '':
            return None, message
        try:
            user = User_Base.objects.get(User_Name=username)
            return user, None
        except User_Base.DoesNotExist:
            return None, 'User does not exist.'

    def authenticate_header(self, request):
        pass

    def get_user_name_from_token(self):
        token = self.get_authorization_token()
        if token:
            try:
                jsonurl = request.urlopen(self.jwt_auth['JWKS_URL'])
                jwks = json.dumps(json.loads(jsonurl.read().decode('utf-8')))
            except HTTPError:
                jwks = json.dumps(self.jwt_auth['JWKS_JSON'])

            rsa = get_default_algorithms()['RS256']
            cert = rsa.from_jwk(jwks)

            try:
                options = {'verify_aud': False}
                result = jwt.decode(token, cert, options=options, algorithms=['RS256'])
                return result['sub'], ''
            except jwt.DecodeError:
                return '', 'Signature Decode Failed.'
            except jwt.ExpiredSignature:
                return '', 'Expired Signature.'
        return '', 'Invalid basic header. No credentials provided.'

    def get_authorization_token(self):
        auth = get_authorization_header(self.request).decode(HTTP_HEADER_ENCODING).split()
        if self.jwt_auth and len(auth) == 2:
            return auth[1] if auth[0].lower() == self.jwt_auth['JWT_AUTH_HEADER_PREFIX'].lower() else None

        return None
