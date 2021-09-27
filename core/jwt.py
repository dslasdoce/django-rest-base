from rest_framework_simplejwt.views import (TokenViewBase,
                                            TokenError,
                                            InvalidToken, status)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import (RefreshToken)
from rest_framework.exceptions import AuthenticationFailed
from apps.user.models import User
from django.db.models import Q


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data["token"] = data.pop("access")
        except AuthenticationFailed:
            error = {"password": "invalid password or email"}
            if username := attrs.get('username', attrs.get('email')):
                username = Q(username=username) | Q(email=username)
                try:
                    User.objects.get(username)
                except User.DoesNotExist:
                    error = {"username": "username or email cannot be found"}

            raise AuthenticationFailed(error)

        return data


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairSerializer
