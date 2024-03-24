from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.
# Events model
class Event(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    start_datetime = models.DateTimeField(_('start datetime'))
    end_datetime = models.DateTimeField(_('end datetime'))
    location = models.CharField(_('location'), max_length=255, blank=True, null=True)
  
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})