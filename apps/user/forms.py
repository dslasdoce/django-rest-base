from django.contrib.auth.forms import PasswordResetForm


class PasswordResetForm(PasswordResetForm):
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)