from django.apps import AppConfig
from django.db.models.signals import pre_delete
from utils.helpers.utils.signal_handlers import cloudinary_image_delete_signal_handlers


class OperationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'operation'
    
    def ready(self):
        from operation import models
        pre_delete.connect(cloudinary_image_delete_signal_handlers, sender=models.Team)
        pre_delete.connect(cloudinary_image_delete_signal_handlers, sender=models.Mentor)
    
