# -*- coding: utf-8 -*-
from rest_framework import serializers
from apps.account.models import Profile
from moon_ml.serializers import BaseSerializer
from allauth.account.adapter import get_adapter
from django.utils.translation import ugettext_lazy as _


class ProfileSerializer(BaseSerializer):
    first_name = serializers.CharField(source='id.first_name')
    last_name = serializers.CharField(source='id.last_name')
    name = serializers.SerializerMethodField()
    email = serializers.CharField(source='id.email')
    password = serializers.CharField(max_length=64, required=False)
    confirmed_password = serializers.CharField(max_length=64, required=False)
    current_password = serializers.CharField(max_length=64, required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = BaseSerializer.Meta.read_only_fields

    def get_name(self, obj):
        return f'{obj.id.first_name} {obj.id.last_name}'

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if (data.get('password')
                and (data.get('password') != data.get('confirmed_password'))):
            raise serializers.ValidationError(
                {'password': _("The two password fields didn't match.")})
        if data.get('password') and not self.instance.id.check_password(
                data.get('current_password')):
            raise serializers.ValidationError(
                {'current_password': _("Invalid old password")})
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = validated_data.pop('id', None)

        # set the new tz now because it will be used in measurements
        new_tz = validated_data.get('timezone')
        if new_tz:
            instance.timezone = new_tz

        if password:
            instance.id.set_password(password)
            instance.id.save()

        if user:
            for attr, value in user.items():
                setattr(instance.id, attr, value)
            instance.id.save()

        return super().update(instance, validated_data)

