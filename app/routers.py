# database_router.py

class AppDatabaseRouter:
    """
    A router to control which database is used for which app's models.
    """

    def db_for_read(self, model, **hints):
        """Directs read operations for certain apps to specific databases."""
        if model._meta.app_label in ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']:
            return 'default'
        return 'mysql'

    def db_for_write(self, model, **hints):
        """Directs write operations for certain apps to specific databases."""
        if model._meta.app_label in ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']:
            return 'default'
        return 'mysql'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensures that certain apps' migrations only affect certain databases."""
        if app_label in ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles']:
            return db == 'default'
        return db == 'mysql'

