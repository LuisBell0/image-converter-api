from .base import *

DEBUG = True
SECRET_KEY = "django-insecure-x+x-cgmf!3y#tmi773s!fv&!%cfx0p&%kk0i29is@%kjv3oyl)"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=3)
}
