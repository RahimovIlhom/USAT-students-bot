from django.db import models
from django.utils.translation import gettext_lazy as _

from hall_app.models import Hall


EVENT_STATUS = (
    ('no_started', _("Boshlanmagan")),
    ('started', _("Boshlandi")),
    ('finished', _("Yakunlangan"))
)


class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Tadbir nomi"))
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="events", verbose_name=_("Tadbir zali"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Tadbir haqida"))
    date = models.DateTimeField(verbose_name=_("Tadbir boshlanish sana va vaqti"))
    default_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Tadbir narxi"))  # Umumiy narx
    status = models.CharField(max_length=10, choices=EVENT_STATUS, default='no_started', verbose_name=_("Tadbir holati"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktikligi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Oxirgi yangilangan vaqti"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = _("Tadbir ")
        verbose_name_plural = _("Tadbirlar")
        db_table = "events"
        ordering = ['-date']
