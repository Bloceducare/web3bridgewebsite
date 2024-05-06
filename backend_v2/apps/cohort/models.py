from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.helpers.models import BaseModelBaseMixin, CloudinaryDeleteMixin
from utils.models import Image
from utils.enums.models import RegistrationStatus
from .helpers.model import testimonial_image_location

# Model
# Course model
class Course(BaseModelBaseMixin, models.Model):  
    name= models.CharField(_('course name'), max_length=1000, blank=False, null=False)
    description= models.TextField(_("description"), blank=False, null=False)
    venue= models.JSONField(_("venue"), null=False, blank=False, default=list, editable=True)
    extra_info= models.TextField(_("extra_info"), blank=False, null=False)
    images= models.ManyToManyField(Image, related_name='related_images')
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name}) >"
    
# Registration openings model
class Registration(BaseModelBaseMixin, models.Model):
    name= models.CharField(_('registration name'), max_length=1000, blank=False, null=False)
    is_open = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    registrationFee = models.CharField(_('registration fee'), max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name} {self.start_date}-{self.end_date}) >"
    
# Participant model
class Participant(BaseModelBaseMixin, models.Model): 
    name= models.CharField(_('full name'), max_length=255, blank=False, null=True)
    wallet_address= models.CharField(_('wallet address'), max_length=255, blank=False, null=False)  
    email= models.CharField(_('participant email'), max_length=255, blank=False, null=False) 
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=RegistrationStatus.choices(), default=RegistrationStatus.PENDING.value) 
    motivation = models.TextField(_("motivation"), blank=False, null=True) 
    achievement = models.TextField(_("achievement"), blank=True, null=True)   
    city = models.CharField(_('city name'), max_length=50, blank=False, null=True)  
    country = models.CharField(_('country name'), max_length=50, blank=False, null=True)  
    duration = models.CharField(_('duration'), max_length=100, blank=False, null=True) 
    gender = models.CharField(_('gender'), max_length=20, blank=False, null=True)  
    github = models.URLField(_('github url'), max_length=250, blank=True, null=True)  
    number = models.CharField(_('phone number'), max_length=20, blank=False, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=True)
    
    class Meta:
        unique_together = ('email', 'registration',)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name}) >"
    
# Testimonial model
class Testimonial(BaseModelBaseMixin, CloudinaryDeleteMixin, models.Model):  
    headline= models.CharField(_('headline'), max_length=1000, blank=False, null=False)
    full_name= models.CharField(_('last name'), max_length=255, blank=False, null=False)
    testimony= models.TextField(_("testimony"), blank=False, null=False)
    picture= models.ImageField(upload_to=testimonial_image_location, blank=False, null=False)
    brief= models.CharField(_('author brief'), max_length=255, blank=False, null=False)
    
    def __str__(self):
        full_name_processed= self.full_name.replace(" ", "_")
        return f"< {type(self).__name__}({full_name_processed})>"
    
    
