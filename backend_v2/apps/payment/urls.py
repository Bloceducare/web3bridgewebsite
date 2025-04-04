from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from .literals import (APP_NAME, PAYMENT_BASE_NAME, DISCOUNT_BASE_NAME)
from . import views 
from django.urls import path, include

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name= APP_NAME
router.register("payment", views.PaymentViewset, basename=PAYMENT_BASE_NAME)
router.register("discount", views.DiscountCodeViewset, basename=DISCOUNT_BASE_NAME)

urlpatterns = [
    path('', include(router.urls)),
    path('/generate-with-api/', views.APIGenerateDiscountCode.as_view(), name='api-generate-discount'),
]