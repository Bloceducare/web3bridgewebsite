from django.db import models
from django.forms import ValidationError
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
    duration = models.CharField(_('duration'), max_length=100, blank=False, default="3 months")
    #One to Many relationship with Registration
    registration = models.ForeignKey('Registration', related_name='courses', on_delete=models.SET_NULL, null=True)
    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name}) >"
    
# Registration openings model
class Registration(BaseModelBaseMixin, models.Model):
    name= models.CharField(_('registration name'), max_length=1000, blank=False, null=False)
    is_open = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    cohort = models.CharField(_('cohort name'), max_length=20, blank=False, null=False, default='Cohort-XIII')
    registrationFee = models.CharField(_('registration fee'), max_length=50, blank=True, null=True)

    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name} {self.start_date}-{self.end_date}) >"
    
# Participant model
class Participant(BaseModelBaseMixin, models.Model): 
    name= models.CharField(_('full name'), max_length=255, blank=False, null=False, default="")
    wallet_address= models.CharField(_('wallet address'), max_length=255, blank=False, null=False)  
    email = models.EmailField(_('participant email'), max_length=255, blank=False, null=False) 
    registration = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=RegistrationStatus.choices(), default=RegistrationStatus.PENDING.value) 
    motivation = models.TextField(_("motivation"), blank=False, null=True) 
    achievement = models.TextField(_("achievement"), blank=False, null=True)   
    city = models.CharField(_('city name'), max_length=50, blank=False, null=True)  
    state = models.CharField(_('state name'), max_length=50, blank=False, null=True)  
    country = models.CharField(_('country name'), max_length=50, blank=False, null=True)   
    gender = models.CharField(_('gender'), max_length=20, blank=False, null=True)  
    github = models.URLField(_('github url'), max_length=250, blank=True, default="")  
    number = models.CharField(_('phone number'), max_length=20, blank=False, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    cohort = models.CharField(_('cohort name'), max_length=20, blank=False, null=False, default='Cohort-XIII')
    payment_status = models.BooleanField(default=False)
    venue = models.CharField(_('venue'), max_length=30, blank=False, null=False, default="online")
    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('email', 'registration',)
        indexes = [
            models.Index(fields=['-created_at'], name='participant_created_at_idx'),
            models.Index(fields=['email'], name='participant_email_idx'),
            models.Index(fields=['registration'], name='participant_registration_idx'),
            models.Index(fields=['course'], name='participant_course_idx'),
            models.Index(fields=['status'], name='participant_status_idx'),
        ]
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name}) >"
   
    
# Testimonial model
class Testimonial(BaseModelBaseMixin, CloudinaryDeleteMixin, models.Model):  
    headline= models.CharField(_('headline'), max_length=1000, blank=True, null=True)
    full_name= models.CharField(_('last name'), max_length=255, blank=False, null=False)
    testimony= models.TextField(_("testimony"), blank=False, null=False)
    picture_link = models.URLField(_('picture link'), max_length=250, blank=True, default="")
    # picture= models.ImageField(upload_to=testimonial_image_location, blank=False, null=False)
    # brief= models.CharField(_('author brief'), max_length=255, blank=False, null=False)

    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        full_name_processed= self.full_name.replace(" ", "_")
        return f"< {type(self).__name__}({full_name_processed})>"
    
    
