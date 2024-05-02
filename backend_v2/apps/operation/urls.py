from django.urls import path, re_path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from .literals import (APP_NAME, TEAM_BASE_NAME, MENTOR_BASE_NAME, PARTNER_BASE_NAME)
from . import views 

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
    
app_name= APP_NAME
router.register("team", views.TeamViewSet, basename=TEAM_BASE_NAME)
router.register("mentor", views.MentorViewSet, basename=MENTOR_BASE_NAME)
router.register("partner", views.PartnerViewSet, basename=PARTNER_BASE_NAME)

urlpatterns= router.urls