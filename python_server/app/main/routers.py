"""Manage multiple databases.

see https://docs.djangoproject.com/en/5.2/topics/db/multi-db/
"""

from django.apps import apps


class DatabaseRouter:
    """Route models to differnt databases."""

    def __init__(self):
        """Instance init."""
        self.app_label_to_db = {}
        for app_conf in apps.get_app_configs():
            if hasattr(app_conf, "database") and hasattr(app_conf, "name"):
                self.app_label_to_db[app_conf.name] = app_conf.database  # type:ignore

    def _db_from_app_label(self, app_label, **hints):
        return self.app_label_to_db.get(app_label, "default")

    def _db_from_model(self, model, **hints):
        app_label = model._meta.app_label
        return self._db_from_app_label(app_label=app_label, **hints)

    def db_for_read(self, model, **hints) -> str:
        """Suggest the database to be used for read operations for model objects."""
        return self._db_from_model(model=model, **hints)

    def db_for_write(self, model, **hints) -> str:
        """Suggest the database to be used for writes of objects of type Model."""
        return self._db_from_model(model=model, **hints)

    def allow_relation(self, model1, model2, **hints) -> bool:
        """Return True if a relation between obj1 and obj2 should be allowed.

        False if the relation should be prevented,
        or None if the router has no opinion.
        This is purely a validation operation, used by foreign key and many to many
        operations to determine if a relation should be allowed between two objects.
        """
        return self._db_from_model(model=model1, **hints) == self._db_from_model(
            model=model2, **hints
        )

    def allow_migrate(self, db, app_label, model_name=None, **hints) -> bool:
        """Determine if migration operation is allowed to run on db.

        Return True if the operation should run, False if it shouldn’t run,
        or None if the router has no opinion.
        """
        return self._db_from_app_label(app_label, **hints) == db
