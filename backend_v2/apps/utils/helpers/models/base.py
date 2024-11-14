from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import cloudinary.uploader


class BaseModelBaseMixin:
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True,)
    timestamp = models.DateTimeField(_("update time"), auto_now=True,)

    def is_instance_exist(self):
        return self.__class__.objects.filter(id=self.id).exists()

    @property
    def current_instance(self):
        return self.__class__.objects.get(id=self.id)
    
    
class CloudinaryDeleteMixin:
    def delete_cloudinary_image(self):
        if self.picture:
            public_id = self.picture.url.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)
    
    
#  image storage location
def image_location(instance, filename):
    return f"{settings.ENVIROMENT}/{instance.__class__.__name__}/{filename}"