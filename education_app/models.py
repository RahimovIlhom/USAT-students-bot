from django.db import models
from django.utils.translation import gettext_lazy as _


class EduDirection(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Ta’lim yo‘nalishi'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'edu_directions'
        verbose_name = _('Ta’lim yo‘nalishi ')
        verbose_name_plural = _('Ta’lim yo‘nalishilari')
        ordering = ['name']


class EduType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Ta’lim turi'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'edu_types'
        verbose_name = _('Ta’lim turi ')
        verbose_name_plural = _('Ta’lim turlari')
        ordering = ['name']
