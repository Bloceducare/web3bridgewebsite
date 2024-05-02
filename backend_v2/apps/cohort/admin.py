from django.contrib import admin
from .models import Course, Registration, Participant, Testimonial

# Register your models here.
admin.site.register(Course)
admin.site.register(Registration)
admin.site.register(Participant)
admin.site.register(Testimonial)