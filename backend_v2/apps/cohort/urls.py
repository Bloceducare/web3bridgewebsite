from django.urls import path, re_path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from .literals import (APP_NAME, COURSE_BASE_NAME, REGISTRATION_BASE_NAME, PARTICIPANT_BASE_NAME, TESTIMONIAL_BASE_NAME)
from . import views 

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name= APP_NAME
router.register("course", views.CouresViewSet, basename=COURSE_BASE_NAME)
router.register("registration", views.RegistrationViewSet, basename=REGISTRATION_BASE_NAME)
router.register("participant", views.ParticipantViewSet, basename=PARTICIPANT_BASE_NAME)
router.register("testimonial", views.TestimonialViewSet, basename=TESTIMONIAL_BASE_NAME)
router.register(r'bulk-email', views.BulkEmailViewSet, basename='bulk-email')


urlpatterns= router.urls