# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.serializers import (
    PasswordResetConfirmSerializer, PasswordResetSerializer,
)
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from apps.user.forms import PasswordResetForm
from django.conf import settings


UserModel = get_user_model()


class SocialLoginCustomSerializer(SocialLoginSerializer):
    token = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    code = None
    access_token = None

    def validate(self, attrs):
        # the SocialLoginSerializer uses access_token field but we renamed
        # it to token so just set access_token = token
        attrs['access_token'] = attrs.get('token')
        val = super().validate(attrs)
        return val


class AppleLoginSerializer(SocialLoginCustomSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def get_social_login(self, adapter, app, token, response):
        request = self._get_request()
        if first_name := self.initial_data.get('first_name'):
            token.user_data['first_name'] = first_name
        if last_name := self.initial_data.get('last_name'):
            token.user_data['last_name'] = last_name

        social_login = adapter.complete_login(
            request, app, token, response=response)
        social_login.token = token
        return social_login


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    confirmed_password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    timezone = serializers.CharField(required=False)

    @staticmethod
    def validate_username(username):
        username = get_adapter().clean_username(username)
        return username

    @staticmethod
    def validate_email(email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    @staticmethod
    def validate_password(password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def save(self, request, timezone=''):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        if timezone:
            self.cleaned_data['timezone'] = timezone

        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # setup_user_email(request, user, [])
        return user


class PasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        return {
            'email_template_name': 'email/user_reset_password.html',
            'extra_email_context': {'site_tag': settings.TAG_LINE}
        }

    def validate_email(self, value):
        value = super().validate_email(value)
        try:
            UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            raise ValidationError('email does not exists')
        return value


class PasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password1 = serializers.CharField(read_only=True)
    new_password2 = serializers.CharField(read_only=True)
    password = serializers.CharField(max_length=128)
    confirmed_password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        attrs['new_password1'] = attrs['password']
        attrs['new_password2'] = attrs['confirmed_password']
        return super().validate(attrs)
