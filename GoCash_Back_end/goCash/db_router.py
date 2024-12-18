class DWBIDataRouter:
    def db_for_read(self, model, **hints):
        """Direct read queries for models in the 'DWBI' app to the data warehouse."""
        if model._meta.app_label == 'dwbi':
            return 'datawarehouse'
        return 'default'

    def db_for_write(self, model, **hints):
        """Prevent writes to the data warehouse."""
        if model._meta.app_label == 'dwbi':
            return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relationships between models in the same database."""
        if obj1._state.db in ('default', 'datawarehouse') and obj2._state.db in ('default', 'datawarehouse'):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure the 'dwbi' app only exists in the 'datawarehouse' database."""
        if app_label == 'dwbi':
            return db == 'datawarehouse'
        return db == 'default'
