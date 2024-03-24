from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.utils.helpers.models import BaseModelBaseMixin

# Create your models here.
# Course model
class Course(BaseModelBaseMixin, models.Model):  

    def __str__(self):
        pass
    
# Registration model
class Registration(BaseModelBaseMixin, models.Model):  
    
    def __str__(self):
        pass
    
# Testimonial model
class Testimonial(BaseModelBaseMixin, models.Model):  

    def __str__(self):
        pass