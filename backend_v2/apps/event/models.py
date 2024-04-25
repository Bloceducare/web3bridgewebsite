from django.db import models

# Create your models here.
# Events model
class Event(models.Model): 
    
    class Meta:
        app_label= "event" 

    def __str__(self):
        return self.title
