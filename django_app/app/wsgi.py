# coding: utf-8
import os
import sys

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
application = get_wsgi_application()
