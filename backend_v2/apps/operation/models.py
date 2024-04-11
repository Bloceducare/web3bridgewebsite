from django.db import models
from utils.helpers.models import BaseModelBaseMixin, CloudinaryDeleteMixin
from django.utils.translation import gettext_lazy as _
from .helpers.model import team_image_location, mentor_image_location, partner_image_location

# Model
# Team model
class Team(BaseModelBaseMixin, CloudinaryDeleteMixin, models.Model):  
    full_name= models.CharField(_('full name'), max_length=1000, blank=False, null=False)
    brief= models.TextField(_("brief"), blank=False, null=False)
    extra_info= models.TextField(_("extra_info"), blank=True, null=True)
    picture= models.ImageField(upload_to=team_image_location, blank=False, null=False)
    
    def __str__(self):
        full_name_processed= self.full_name.replace(" ", "_")
        return f"< {type(self).__name__}({full_name_processed}) >"
    
# Mentor model
class Mentor(BaseModelBaseMixin, CloudinaryDeleteMixin, models.Model):  
    full_name= models.CharField(_('full name'), max_length=1000, blank=False, null=False)
    repo= models.URLField(_('repo url'), max_length=1000, blank=False, null=False)
    extra_info= models.TextField(_("extra_info"), blank=True, null=True)
    picture= models.ImageField(upload_to=mentor_image_location, blank=False, null=False)
    
    def __str__(self):
        full_name_processed= self.full_name.replace(" ", "_")
        return f"< {type(self).__name__}({full_name_processed}) >"
    
# Partner model
class Partner(BaseModelBaseMixin, CloudinaryDeleteMixin, models.Model):  
    name= models.CharField(_('full name'), max_length=1000, blank=False, null=False)
    url= models.URLField(_('repo url'), max_length=1000, blank=True, null=True)
    extra_info= models.TextField(_("extra_info"), blank=True, null=True)
    picture= models.ImageField(upload_to=partner_image_location, blank=True, null=True)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name}) >"