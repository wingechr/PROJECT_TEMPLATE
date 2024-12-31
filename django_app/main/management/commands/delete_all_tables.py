from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Reset the database by dropping all tables"

    def handle(self, *args, **options):
        db_backend = connection.vendor

        if db_backend == "postgresql":
            self.drop_tables_postgresql()
        elif db_backend == "sqlite":
            self.drop_tables_sqlite()
        else:
            raise NotImplementedError(db_backend)

    def drop_tables_postgresql(self):
        with connection.cursor() as cursor:
            # Drop all tables for PostgreSQL using dynamic SQL
            cursor.execute(
                """
                DO $$ DECLARE
                  r RECORD;
                BEGIN
                  FOR r IN (
                    SELECT tablename FROM pg_tables WHERE schemaname = 'public'
                  ) LOOP
                    EXECUTE 'DROP TABLE IF EXISTS public.' || r.tablename || ' CASCADE';
                  END LOOP;
                END $$;
            """
            )

    def drop_tables_sqlite(self):
        with connection.cursor() as cursor:
            # Get all tables from the SQLite database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_names = [t[0] for t in cursor.fetchall()]
            # ignore undeletabla
            table_names = [t for t in table_names if t not in ["sqlite_sequence"]]

            # Disable foreign key checks because there is no delete cascade
            cursor.execute("PRAGMA foreign_keys = OFF;")
            # Drop each table in SQLite
            for table_name in table_names:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            cursor.execute("PRAGMA foreign_keys = ON;")
