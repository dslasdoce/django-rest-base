from rest_framework.serializers import ValidationError
import abc

__shape_types__ = {}


class ShapeTypeMetaclass(abc.ABCMeta):
    def __new__(meta, name, bases, attrs):
        __shape_types__[name] = cls = super().__new__(meta, name, bases, attrs)
        return cls


class ShapeTypeAbstract(metaclass=ShapeTypeMetaclass):
    parameters = []
    __shape__classes = []

    def __init__(self, parameters):
        if not len(self.parameters):
            raise NotImplementedError('PARAMETERS must be declared')
        for parameter in self.parameters:
            try:
                value = parameters[parameter]
                if value:
                    setattr(self, parameter, value)
                else:
                    raise ValidationError({
                        parameter:
                            f'{self.__class__.__name__} '
                            f'parameter "{parameter}" cannot be "0" or "null"'
                         }
                    )
            except KeyError:
                raise ValidationError({
                    parameter:
                        f'{self.__class__.__name__} '
                        f'parameter "{parameter}" must be declared'})

    @classmethod
    def children_names(cls):
        return [c.__name__ for c in cls.__subclasses__()]

    @classmethod
    def child_classes(cls):
        return {k: v for k, v in __shape_types__.items()
                if v != ShapeTypeAbstract}

    @classmethod
    def as_choices(cls):
        return [(k, k) for k in cls.child_classes()]

    @classmethod
    def from_shape_type_name(cls, name):
        return __shape_types__.get(name)

    @abc.abstractmethod
    def area(self):
        pass

    @abc.abstractmethod
    def perimeter(self):
        pass
