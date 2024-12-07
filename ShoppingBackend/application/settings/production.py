import os

from .defaults import *


DEBUG = True
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT')
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT')

