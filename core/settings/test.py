from core.settings.base import *

ENCRYPT = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your-project-name',
        'USER': 'your-user-name',
        'PASSWORD': 'your-password',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432')
    }
}
