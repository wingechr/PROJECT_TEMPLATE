class AppDatabaseRouter:
    """
    Database router that routes all operations for models in a specific app
    to a designated database.
    """

    app_label = ""
    database = ""

    def db_for_read(self, model, **hints):
        """
        Attempts to read model objects from other_db if they belong to myapp.
        """
        if model._meta.app_label == self.app_label:
            return self.database
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write model objects to other_db if they belong to myapp.
        """
        if model._meta.app_label == self.app_label:
            return self.database
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the specific app or if neither is.
        """
        in_app1 = obj1._meta.app_label == self.app_label
        in_app2 = obj2._meta.app_label == self.app_label

        # Allow if both objects are in our app (same database)
        if in_app1 and in_app2:
            return True
        # Allow if neither object is in our app (different database)
        elif not in_app1 and not in_app2:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the app's models are only migrated on the other_db database.
        """
        if app_label == self.app_label:
            return db == self.database
        return db == "default"
