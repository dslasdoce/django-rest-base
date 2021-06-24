from django.shortcuts import render
from rest_auth.registration.views import RegisterView


# Create your views here.
class RegisterView(RegisterView):
    serializer_class = RegisterSerializer

    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        token = TokenObtainPairSerializer()
        refresh = token.get_token(user)
        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data["token"] = data.pop("access")

        return data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        emailconfirmation = EmailConfirmationHMAC(user)
        get_adapter().send_confirmation_mail(self.request,
                                             emailconfirmation, False)
        return user
