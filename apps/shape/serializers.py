from core.serializers import BaseSerializer
from apps.shape.models import Shape
from rest_framework import serializers


class ShapeSerializer(BaseSerializer):
    area = serializers.SerializerMethodField()
    perimeter = serializers.SerializerMethodField()

    class Meta:
        model = Shape
        fields = '__all__'
        read_only_fields = BaseSerializer.Meta.read_only_fields

    @staticmethod
    def get_area(obj):
        return obj.area

    @staticmethod
    def get_perimeter(obj):
        return obj.perimeter
