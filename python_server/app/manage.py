#!/usr/bin/env python3

import os
import sys

# BASE_DIR: contains manage.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# LOCAL_DATA_DIR: contains local_settings.py
LOCAL_DATA_DIR = os.path.dirname(BASE_DIR) + "/_local"
sys.path.append(LOCAL_DATA_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
