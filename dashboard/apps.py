from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self, *args, **kwargs):
        import dashboard.signals   #noqa 
        super_ready = super().ready(*args, **kwargs)
        return super_ready
    