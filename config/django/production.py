from config.env import env
from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=False)
SECRET_KEY = env("SECRET_KEY")
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
SESSION_COOKE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# BACKBLAZE B2 SETTINGS
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT = env('AWS_S3_ENDPOINT')
DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/day',
        'user': '50/day'
    }
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

SIMPLE_JWT = {
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10)
}
