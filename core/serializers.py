import logging
import re
from rest_framework import serializers
from core.models import BaseModel
from enum import IntFlag


LOG = logging.getLogger(__name__)


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = ('date_created', 'date_updated')
        read_only_fields = ('id', 'date_created', 'date_updated', 'user')


class IntFlag(IntFlag):
    """
    This creates custom methods for the Bitwise flags
    """
    @classmethod
    def items(cls):
        return [(member.value, name)
                for name, member in cls.__members__.items()]

    @classmethod
    def as_name_list(cls, lower=False, **kwargs):
        return [cls.to_representation(name).lower() if lower
                else cls.to_representation(name)
                for name, _ in cls.__members__.items()]

    @classmethod
    def as_values_list(cls):
        return [value for _, value in cls.__members__.items()]

    @classmethod
    def as_raw_name_list(cls):
        return [name for name, _ in cls.__members__.items()]

    @classmethod
    def to_representation(cls, name):
        if name is not None or isinstance(name, str):
            return (
                name.title().replace('_', ' ')
                if not getattr(cls, f'repr_{name.lower()}', None)
                else getattr(cls, f'repr_{name.lower()}')()
            )
        else:
            return name

    @classmethod
    def as_choices(cls, key_type=str):
        # sample output: [('Name1', 'name1'), ('Name2', 'name2']
        if key_type == str:
            return [(name, cls.to_representation(name))
                    for name, _ in cls.__members__.items()]
        # sample output: [(1, 'name1'), (2, 'name2']
        if key_type == int:
            return [(member.value, name.lower())
                    for name, member in cls.__members__.items()]

    def extra_properties(self):
        return None


class IntFlagHandler:
    """
    This serves as middleware to convert bitwise flags to values and
    vice versa
    """
    def __init__(self, *flags):
        self.__flag_set = self.enum_class(0)
        self.__flag_class = self.enum_class
        self.__flag_list = []
        error_list = []

        for flag in flags:
            try:
                if isinstance(flag, int):
                    flag_obj = self.enum_class(flag)
                else:
                    flag_processed = re.sub(r'[^\w\\]', '_', flag)
                    flag_obj = self.enum_class[flag_processed.lower()]
                self.__flag_set |= flag_obj
                self.__flag_list.append(flag_obj.name)
            except KeyError:
                error = True
                # try using choices and exact representations
                for k, v in self.enum_class.as_choices():
                    if v == flag:
                        flag_obj = self.enum_class[k]
                        self.__flag_set |= flag_obj
                        self.__flag_list.append(flag_obj.name)
                        error = False
                        break
                if error:
                    error_list.append(f'{flag} is not a valid choice')
        if error_list:
            raise serializers.ValidationError(error_list)

    @property
    def flag_list(self):
        return [self.enum_class.to_representation(name)
                for name in self.__flag_list]

    @property
    def flag_names(self):
        return [name for name in self.__flag_list]

    @property
    def single_flag_name(self):
        """
        This only works if you are referring to one and only one enum
        """
        return self.enum_class.to_representation(self.flags.name)

    @classmethod
    def from_value(cls, value):
        """
        Instantiate the class from a bitwise value. This is commonly used
        by serializer's to_representation since the internal value saved is
        an integer and we convert that integer value into actual BitFlag class
        so we can access each flags later on
        """
        value = value if value else 0
        flags = [flag.name for flag in cls.enum_class if flag.value & value]
        return cls(*flags)

    @property
    def flags(self):
        """
        Returns the flags that were combined
        """
        return self.__flag_set

    @property
    def value(self):
        """
        Returns the value of the BitFlag after performing XOR on all flags
        """
        return self.flags.value


class BitFlagChoiceField(serializers.ChoiceField):
    def __init__(self, *args, bitflag_class=None, **kwargs):
        self.bitflag_class = bitflag_class

        if not bitflag_class:
            raise TypeError('missing required keyword argument "bitflag_class"')
        kwargs['choices'] = self.bitflag_class.as_choices()
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        return self.bitflag_class.from_value(value).single_flag_name

    def to_internal_value(self, data):
        if isinstance(data, list) or isinstance(data, tuple):
            return self.bitflag_class(*data).value
        else:
            return self.bitflag_class(data).value


class BitFlagMultipleChoiceField(BitFlagChoiceField,
                                 serializers.MultipleChoiceField):
    def to_representation(self, value):
        return self.bitflag_class.from_value(value).flag_list

    def to_internal_value(self, data):
        return self.bitflag_class(*data).value
