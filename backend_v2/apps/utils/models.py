from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from .helpers.models import image_location

class Image(models.Model):
    picture = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to=image_location
    )
    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)