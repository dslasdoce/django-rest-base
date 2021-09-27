from rest_auth.views import (
    PasswordResetView, PasswordChangeView, PasswordResetConfirmView)
from django.utils.translation import ugettext_lazy as _
from apps.user.serializers import (
    PasswordResetConfirmSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


class PasswordChangeView(PasswordChangeView):
    pass


class PasswordResetView(PasswordResetView):
    authentication_classes = (JWTAuthentication,)

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response


class PasswordResetConfirmView(PasswordResetConfirmView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    allowed_methods = ('PATCH', )

    def patch(self, request, *args, **kwargs):
        data = {
            'password': request.data.get('password'),
            'confirmed_password': request.data.get('confirmed_password'),
            **kwargs
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )
