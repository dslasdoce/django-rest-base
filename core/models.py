from django.db import models
from django.core import checks
from core.managers import BaseManager


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    objects = BaseManager()

    class Meta:
        abstract = True


class BitFlagField(models.IntegerField):
    """
    This is just a pass thru class to indicate that an integer field uses
    bitflags for values
    """

    def __init__(self, *args, **kwargs):
        if enum_handler := kwargs.pop('enum_handler', None):
            self.enum_handler = enum_handler
        else:
            self.enum_handler = None
        super().__init__(*args, **kwargs)

    def single_flag_name(self):
        return self.enum_handler.from_value(self)

    def check(self, **kwargs):
        # Call the superclass
        errors = super().check(**kwargs)

        # Do some custom checks and add messages to `errors`:
        errors.extend(self._check_enum_handler(**kwargs))

        # Return all errors and warnings
        return errors

    def _check_enum_handler(self, **kwargs):
        if self.enum_handler is None:
            return [
                checks.Error(
                    ' must declare enum_handler attribute',
                    obj=self,
                    id='fields.E120',
                )
            ]
        # When no error, return an empty list
        return []
