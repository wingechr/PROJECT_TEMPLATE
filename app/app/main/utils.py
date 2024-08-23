from django.db import connections
from django.db.migrations.recorder import MigrationRecorder
from main import __version__


def get_info():
    def _get_current_migration_revision_id(app_name):
        connection = connections["default"]
        recorder = MigrationRecorder(connection)
        latest_migration = (
            recorder.migration_qs.filter(app=app_name).order_by("-applied").first()
        )
        if latest_migration:
            return latest_migration.name
        return None

    data = {}
    data["version:app"] = __version__
    data["version:dbschema:main"] = _get_current_migration_revision_id("main")

    return data
