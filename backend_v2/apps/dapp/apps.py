from django.apps import AppConfig
from django.db.models.signals import pre_delete
from utils.helpers.utils.signal_handlers import cloudinary_image_delete_signal_handlers


class DappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dapp'
    
    def ready(self):
        from dapp import models
        pre_delete.connect(cloudinary_image_delete_signal_handlers, sender=models.Dapp)
