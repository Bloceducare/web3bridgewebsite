from django.urls import path, re_path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from .literals import (APP_NAME, DAPP_BASE_NAME)
from . import views 

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
    
app_name= APP_NAME
router.register("", views.EventViewSet, basename=DAPP_BASE_NAME)

urlpatterns= router.urls