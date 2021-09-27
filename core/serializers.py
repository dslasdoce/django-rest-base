import logging
from rest_framework import serializers
from core.models import BaseModel


LOG = logging.getLogger(__name__)


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = ('date_created', 'date_updated')
        read_only_fields = ('id', 'date_created', 'date_updated', 'user')
