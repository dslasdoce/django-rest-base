from core.views import BaseUserModelViewSet
from apps.shape import serializers as shape_serializer
from apps.shape import models as shape_models


class ShapeViewSet(BaseUserModelViewSet):
    serializer_class = shape_serializer.ShapeSerializer
    queryset = shape_models.Shape.objects.all().select_related('user')
