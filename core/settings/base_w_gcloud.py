from core.settings.local import *
import json
from google.oauth2 import service_account


# Gcloud Storage Setup
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'your-project-name-bucket'
GS_CREDENTIALS = os.environ.get('GS_CREDENTIALS', '{}')
GS_CREDENTIALS = json.loads(GS_CREDENTIALS)
with open('gsc.json', 'w') as f:
    json.dump(GS_CREDENTIALS, f)
GS_CREDENTIALS = service_account.Credentials.from_service_account_file('gsc.json')
