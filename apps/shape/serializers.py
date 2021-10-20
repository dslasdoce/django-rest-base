from core.serializers import BaseSerializer
from apps.shape.models import Shape
from rest_framework import serializers


class ShapeSerializer(BaseSerializer):
    area = serializers.ReadOnlyField()
    perimeter = serializers.ReadOnlyField()

    class Meta:
        model = Shape
        fields = '__all__'
