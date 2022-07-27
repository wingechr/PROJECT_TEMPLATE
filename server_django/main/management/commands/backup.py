import datetime
import logging
import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

BACKUP_DIR = settings.LOCAL_ROOT + "/backups"


class Command(BaseCommand):
    help = "Create a backup of the database"

    def handle(self, *args, **options):
        if settings.DEFAULT_DATABASE["ENGINE"] != "django.db.backends.sqlite3":
            raise CommandError("Backups only implemented for sqlite databases")
        db_path = settings.DEFAULT_DATABASE["NAME"]

        if not os.path.exists(BACKUP_DIR):
            logging.info("creating backup dir: %s", BACKUP_DIR)
            os.makedirs(BACKUP_DIR)

        backup_db_path = os.path.join(
            BACKUP_DIR,
            "backup_%s.sqlite3" % datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        )
        logging.info("creating backup: %s", backup_db_path)
        shutil.copy(db_path, backup_db_path)
