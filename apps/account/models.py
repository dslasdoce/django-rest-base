from django.db import models
from moon_ml.models import BaseModel
from moon_ml.utils import file_upload_to
from moon_ml.managers import BaseManager
from apps.user.models import User
from django.utils import timezone
import pytz


class Profile(BaseModel):
    DEFAULT_USER_TIMEZONE = 'Australia/Melbourne'
    id = models.OneToOneField(User, db_column='id',
                              related_name='profile',
                              on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to=file_upload_to, null=True, blank=True)
    timezone = models.CharField(
        max_length=64, default=DEFAULT_USER_TIMEZONE,
        choices=[(tz, tz) for tz in pytz.all_timezones], )

    objects = BaseManager()

    class Meta:
        db_table = "account_profiles"

    @property
    def my_timezone(self):
        return pytz.timezone(self.timezone)

    @property
    def local_datetime(self):
        return timezone.now().astimezone(self.my_timezone)



