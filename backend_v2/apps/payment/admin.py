from django.contrib import admin

from .models import DiscountCode, Payment, DiscountCodeUsage

# Register your models here.
admin.site.register(DiscountCode)
admin.site.register(Payment)
admin.site.register(DiscountCodeUsage)