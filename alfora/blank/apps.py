from django.apps import AppConfig # type: ignore


class BlankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blank'
