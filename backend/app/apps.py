from django.apps import AppConfig
import app.signals as signal

class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Рецепты'

    def ready(self):
        signal
