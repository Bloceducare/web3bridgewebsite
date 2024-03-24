from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModelBaseMixin:
    created_at = models.DateTimeField(_("creation time"), auto_now_add=True,)
    timestamp = models.DateTimeField(_("update time"), auto_now=True,)

    def is_instance_exist(self):
        return self.__class__.objects.filter(id=self.id).exists()

    @property
    def current_instance(self):
        return self.__class__.objects.get(id=self.id)