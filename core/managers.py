from django.db import models


class BaseQuerySet(models.QuerySet):
    """
    Create base query methods here so it can be used globally
    """
    pass


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db).all()

