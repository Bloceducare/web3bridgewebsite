from django.db import models
from utils.helpers.models import BaseModelBaseMixin, CloudinaryDeleteMixin
from .helpers.model import dapp_image_location
from django.utils.translation import gettext_lazy as _


# Model
# dapp model
class Dapp(BaseModelBaseMixin, CloudinaryDeleteMixin, models.Model):  
    name= models.CharField(_('dapp name'), max_length=250, blank=False, null=False)
    url= models.URLField(_('dapp url'), max_length=1000, blank=False, null=False)
    description= models.TextField(_("description"), blank=False, null=False)
    picture= models.ImageField(upload_to=dapp_image_location, blank=False, null=False)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name}) >"