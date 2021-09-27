from core.settings.base import *

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
        'rest_framework.authentication.SessionAuthentication', )
