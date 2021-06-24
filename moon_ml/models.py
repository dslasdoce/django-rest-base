from django.db import models
from moon_ml.managers import BaseManager


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    objects = BaseManager()

    class Meta:
        abstract = True
