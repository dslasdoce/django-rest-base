from django.db import models
from core.models import BaseModel
from apps.shape.types import ShapeTypeAbstract
from apps.user.models import User
from rest_framework.serializers import ValidationError


class Shape(BaseModel):
    # list the parameter required by shape types here for easy access. will be
    # useful once we add more shapes like trapezoid that has 2 bases
    __parameter_fields = ['length', 'width']

    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=32,
                            choices=ShapeTypeAbstract.as_choices())

    # shape PARAMETERS. for now we only need length and width
    # it is better to just have each possible parameter declared here instead
    # of a JSON field that can hold variable parameter types so we can easily
    # do analysis/queries later like clustering the by shapes and sizes
    length = models.FloatField(null=True)
    width = models.FloatField(null=True)

    def __str__(self):
        return f'Shape {self.id} ({self.type}) - {self.name}'

    @property
    def type_class(self):
        return ShapeTypeAbstract.from_shape_type_name(self.type)

    @property
    def parameters(self):
        return {p: getattr(self, p) for p in self.__parameter_fields}

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
