from main.routers import AppDatabaseRouter


class DataAppDatabaseRouter(AppDatabaseRouter):
    app_label = "data"
    database = "data"
