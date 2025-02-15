from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_auth = JWTAuthentication()
        access_token = request.COOKIES.get('access_token')

        if access_token:
            try:
                validated_token = jwt_auth.get_validated_token(access_token)
                user = jwt_auth.get_user(validated_token)
                request.user = user
            except AuthenticationFailed:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
