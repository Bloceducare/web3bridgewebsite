from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from .literals import APP_NAME, HUB_REGISTRATION_BASE_NAME
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = APP_NAME
router.register("space", views.HubSpaceViewSet, basename="hub-space")
router.register("registration", views.HubRegistrationViewSet, basename=HUB_REGISTRATION_BASE_NAME)
router.register("checkin", views.CheckInViewSet, basename="hub-checkin")

urlpatterns = router.urls

