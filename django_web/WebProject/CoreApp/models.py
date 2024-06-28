from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=50)
    monitor_hosts = models.BooleanField(default=False)
    monitor_containers = models.BooleanField(default=False)

    def __str__(self):
        return self.username
