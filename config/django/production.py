from config.env import env
from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=False)
SECRET_KEY = env("SECRET_KEY")
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
SESSION_COOKE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
