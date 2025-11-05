from django.apps import apps


class DatabaseRouter:
    def __init__(self):
        self.app_label_to_db = {}
        for app_conf in apps.get_app_configs():
            if hasattr(app_conf, "database") and hasattr(app_conf, "name"):
                self.app_label_to_db[app_conf.name] = app_conf.database

    def _db_from_app_label(self, app_label, **hints):
        return self.app_label_to_db.get(app_label, "default")

    def _db_from_model(self, model, **hints):
        app_label = model._meta.app_label
        return self._db_from_app_label(app_label=app_label, **hints)

    def db_for_read(self, model, **hints) -> str:
        return self._db_from_model(model=model, **hints)

    def db_for_write(self, model, **hints) -> str:
        return self._db_from_model(model=model, **hints)

    def allow_relation(self, model1, model2, **hints) -> bool:
        return self._db_from_model(model=model1, **hints) == self._db_from_model(
            model=model2, **hints
        )

    def allow_migrate(self, db, app_label, model_name=None, **hints) -> bool:
        return self._db_from_app_label(app_label, **hints) == db
