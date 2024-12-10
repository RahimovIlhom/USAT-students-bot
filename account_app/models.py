from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='users/images/', null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Foydalanuvchi ')
        verbose_name_plural = _('Foydalanuvchilar')
