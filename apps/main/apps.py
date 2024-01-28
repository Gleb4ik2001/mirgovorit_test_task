from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name= 'главное приложение'

    # def  ready(self) -> None:
    #     from . import signals
    #     return super().ready()
