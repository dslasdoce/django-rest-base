from django.db import models
from core.models import BaseModel
from apps.shape.types import ShapeTypeAbstract
from apps.user.models import User
from rest_framework.serializers import ValidationError


class Shape(BaseModel):
    """
    To add types:
        1. create your shape module under the shape/types dir
        2. define your shape class by inheriting ShapeTypeAbstract and
           making sure you implement the abstract methods and required attrs
    """

    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=32,
                            choices=ShapeTypeAbstract.as_choices())

    # different shapes will have different parameters
    # (e.g. triangle only needs 3 sides
    # but trapezoid will need base 1, base 2, side_1, side_2)
    parameters = models.JSONField()

    def __str__(self):
        return f'Shape {self.id} ({self.type}) - {self.name}'

    @property
    def type_class(self):
        return ShapeTypeAbstract.from_shape_type_name(self.type)

    def save(self, *args, **kwargs):
        # make sure that the shape being created has all the abstract method
        # needed for calculations
        try:
            self.type_class(self.parameters)
        except TypeError:
            raise ValidationError(
                {'type': 'this shape type is missing abstract methods'})
        else:
            super().save(*args, **kwargs)

    @property
    def area(self):
        return self.type_class(self.parameters).area()

    @property
    def perimeter(self):
        return self.type_class(self.parameters).perimeter()
