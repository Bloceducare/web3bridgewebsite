from django.db import models
from .helpers.models import image_location

class Image(models.Model):
    picture = models.ImageField(upload_to=image_location)