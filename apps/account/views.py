from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from allauth.account import app_settings as allauth_settings
from core.jwt import TokenObtainPairSerializer
from core.views import BaseUserModelViewSet, BaseOneToOneViewSet
from apps.account.models import Profile
from apps.account.serializers import ProfileSerializer
from apps.user.serializers import RegistrationSerializer
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.auth import logout
from core.permissions import PublicCreatePermission
from rest_auth.views import PasswordResetView
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProfileViewSet(BaseUserModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (PublicCreatePermission, )

    def get_queryset(self):
        return Profile.objects.filter(id=self.request.user)

    def perform_destroy(self, instance):
        instance.id.delete()

    def post_create(self, user):
        self.kwargs['pk'] = user.id
        return super().get_object()

    def get_serializer_class(self):
        # if self.action == 'my_profile':
        #     return MyProfileSerializer
        if self.request.method == 'POST':
            return RegistrationSerializer
        else:
            return self.serializer_class

    def get_response_data(self, user):
        if (allauth_settings.EMAIL_VERIFICATION ==
                allauth_settings.EmailVerificationMethod.MANDATORY):
            return {"detail": _("Verification e-mail sent.")}

        token = TokenObtainPairSerializer()
        refresh = token.get_token(user)
        serializer = self.serializer_class(user.profile)
        data = serializer.data
        data['token'] = str(refresh.access_token)

        return data

    def perform_create(self, serializer):
        extra_kwargs = {}
        ip_address = self.request.META.get('REMOTE_ADDR')
        try:
            g = GeoIP2()
            details = g.city(ip_address)
            if details:
                if timezone := details.get('time_zone'):
                    extra_kwargs['timezone'] = timezone
        except:
            pass

        user = serializer.save(self.request, **extra_kwargs)
        return user

    def create(self, request, *args, **kwargs):
        logout(self.request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logout(self.request)
        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class MyProfileViewSet(BaseOneToOneViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def my_profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)


class PasswordResetView(PasswordResetView):
    authentication_classes = (JWTAuthentication,)

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response
