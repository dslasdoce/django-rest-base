from django.contrib import admin
from apps.account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('id__email', )
    autocomplete_fields = ('id', )
    list_display = ('id', )
