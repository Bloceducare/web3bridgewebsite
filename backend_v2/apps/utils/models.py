from django.db import models

# Create your models here.
from .helpers.models import image_location

from django.db import models
from .helpers.models import image_location

class Image(models.Model):
    image = models.ImageField(upload_to=image_location)