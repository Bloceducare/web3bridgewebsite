from django.db import models
from django.utils import timezone


class Event(models.Model): 
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(default=timezone.now())
    time = models.TimeField(default=timezone.now())
    time_zone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event/images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label= "event" 

    def __str__(self):
        return self.title
