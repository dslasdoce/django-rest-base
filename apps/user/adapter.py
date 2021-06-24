# -*- coding: utf-8 -*-
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist
from django.urls import reverse
from allauth.utils import build_absolute_uri
from allauth.account.utils import user_username, user_email
from django.apps import apps as django_apps
from allauth.account.adapter import get_adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from requests.exceptions import HTTPError
from allauth.socialaccount.providers.apple.views import (
    AppleOAuth2Adapter, SocialToken)
import requests
import hashlib
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Group


User = get_user_model()


def user_field(user, field, *args):
    """
    Gets or sets (optional) user model fields. No-op if fields do not exist.
    """
    if not field:
        return
    try:
        field_meta = User._meta.get_field(field)
        max_length = field_meta.max_length
    except FieldDoesNotExist:
        if not hasattr(user, field):
            return
        max_length = None
    if args:
        # Setter
        v = args[0]
        if v:
            try:
                v = v[0:max_length]
            except TypeError:
                v = v
        setattr(user, field, v)
    else:
        # Getter
        return getattr(user, field)


class AccountAdapter(DefaultAccountAdapter):
    """
    This account adapter is used whenever we create new user account. Since
    we created a custom user model based on django's abstract model, this
    class helps in making sure that all registration uses the same
    methods (i.e. creating profiles, setting default username, etc.)
    """
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        user_email(user, email)
        user_username(user, username)
        user_field(user, 'first_name', first_name)
        user_field(user, 'last_name', last_name)

        if 'password' in data:
            user.set_password(data["password"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)

        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        extra_profile_details = {}
        timezone_ = data.get('timezone')
        if timezone_:
            extra_profile_details['timezone'] = timezone_

        self.create_profile(user, **extra_profile_details)

        return user

    def create_profile(self, user, **kwargs):
        Profile = django_apps.get_model(settings.USER_PROFILE_MODEL)
        Profile.objects.get_or_create(id=user, **kwargs)

        # add group
        user.groups.add(
            Group.objects.filter(name=settings.DEFAULT_GROUP_NAME).first())

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "verify-email",
            args=[emailconfirmation.key])
        ret = build_absolute_uri(
            request,
            url)
        return ret


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Override the social account save user so we can create profile here
        after saving the user
        """
        user = super().save_user(request, sociallogin, form)
        if extra_data := getattr(sociallogin.account, 'extra_data', None):
            if first_name := extra_data.get('first_name'):
                user.first_name = first_name
            if last_name := extra_data.get('last_name'):
                user.last_name = last_name
            user.save()
        get_adapter().create_profile(user)


class GoogleOAuth2Adapter(GoogleOAuth2Adapter):
    token_url = 'https://oauth2.googleapis.com/tokeninfo'

    def complete_login(self, request, app, token, **kwargs):
        try:
            resp = requests.get(
                self.profile_url,
                params={"access_token": token.token, "alt": "json"},
            )
            resp.raise_for_status()
        except HTTPError:
            resp = requests.get(
                self.token_url,
                params={"id_token": token.token, "alt": "json"},
            )
        resp.raise_for_status()
        extra_data = resp.json()
        if not extra_data.get('id'):
            extra_data['id'] = hashlib.md5(extra_data['email'].encode()).hexdigest()
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login


class AppleOAuth2Adapter(AppleOAuth2Adapter):
    def parse_token(self, data):
        token = SocialToken(
            token=data["access_token"],
        )
        token.token_secret = data.get("refresh_token", "")

        expires_in = data.get(self.expires_in_key)
        if expires_in:
            token.expires_at = timezone.now() + timedelta(seconds=int(expires_in))

        # `user_data` is a big flat dictionary with the parsed JWT claims
        # access_tokens, and user info from the apple post.
        identity_data = self.get_verified_identity_data(data["access_token"])
        token.user_data = {**data, **identity_data}

        return token
