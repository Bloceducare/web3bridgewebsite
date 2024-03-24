from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.utils.helpers.models import BaseModelBaseMixin

# Model
# Course model
class Course(BaseModelBaseMixin, models.Model):  

    def __str__(self):
        pass
    
# Registration model
class Registration(BaseModelBaseMixin, models.Model):  
    
    def __str__(self):
        pass
    
# Testimonial 
# Testimonial image storage location
def testimonial_image_location(instance, filename):
    return f"Cohort/Testimonial/{instance.last_name}_{instance.first_name}/{filename}"
    
# Testimonial model
class Testimonial(BaseModelBaseMixin, models.Model):  
    headline= models.CharField(_('headline'), max_length=1000, blank=False, null=False)
    last_name= models.CharField(_('last name'), max_length=255, blank=False, null=False)
    first_name= models.CharField(_('first name'), max_length=255, blank=False, null=False)
    testimony= models.TextField(_("testimony"), blank=False, null=False)
    picture= models.ImageField(upload_to=testimonial_image_location, blank=False, null=False)
    brief= models.CharField(_('author brief'), max_length=255, blank=False, null=False)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.last_name} {self.first_name}) >"
    
    
        
    
