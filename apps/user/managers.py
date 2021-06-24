from django.contrib.auth.base_user import BaseUserManager
from allauth.account.adapter import get_adapter
from django.db.models import manager


class ProfileManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('id')


class UserManager(BaseUserManager):
    """
    This is used for the custom User model which was adapted from django's
    AbstractUser
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        Note: Use only for dev purposes
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user_adapter = get_adapter()
        user_adapter.create_profile(user)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset()

