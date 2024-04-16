from django.contrib import admin
from .models import Team, Mentor, Partner

# Register your models here.
admin.site.register(Team)
admin.site.register(Mentor)
admin.site.register(Partner)