from django.contrib import admin

from .models import DiscountCode, Payment

# Register your models here.
admin.site.register(DiscountCode)
admin.site.register(Payment)