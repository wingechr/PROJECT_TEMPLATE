#!/usr/bin/env python3

import os
import sys

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASE_DIR)

    ROOT_DIR = os.path.dirname(BASE_DIR)
    sys.path.append(ROOT_DIR)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
