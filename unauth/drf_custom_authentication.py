
from rest_framework import authentication
from rest_framework import exceptions

from unauth.utils import validate_user_jwt


class UnauthAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", "")
        try:
            return validate_user_jwt(token), None
        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed('Invalid token')
