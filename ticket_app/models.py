from datetime import timedelta
from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _


class Ticket(models.Model):
    user = models.ForeignKey('user_app.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Foydalanuvchi'))
    seat = models.ForeignKey('hall_app.Seat', on_delete=models.CASCADE, verbose_name=_('O‘rindiq'))
    event = models.ForeignKey('event_app.Event', on_delete=models.CASCADE, verbose_name=_('Tadbir'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Tadbir narxi"))
    is_available = models.BooleanField(default=True, verbose_name=_("Bo‘sh o‘rindiqmi?"))
    is_paid = models.BooleanField(default=False, verbose_name=_("To‘landimi?"))
    is_booking = models.BooleanField(default=False, verbose_name=_("Bron qilinganmi?"))
    booking_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Bron qilingan vaqti"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo‘shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Oxirgi yangilangan vaqti'))

    def save(self, *args, **kwargs):
        if self.is_booking and not self.booking_at:
            self.booking_at = now()
        elif not self.is_booking:
            self.booking_at = None
        super().save(*args, **kwargs)

    def release_booking_if_expired(self):
        """Bron qilingan vaqti 15 daqiqadan oshgan bo'lsa, bronni ochadi."""
        if self.is_booking and self.booking_at:
            if now() > self.booking_at + timedelta(minutes=15):
                self.is_available = True
                self.is_booking = False
                self.booking_at = None
                self.user = None
                self.save()

    def __str__(self):
        user_name = self.user.student.fullname if self.user else "Foydalanuvchi yo'q"
        return f"{user_name} - {self.event.name} - {self.seat.number}"

    class Meta:
        verbose_name = _("Bilet")
        verbose_name_plural = _("Biletlar")
        db_table = "tickets"
        ordering = ['event__date', 'seat__line__sector__name', 'seat__line__number', 'seat__section__number', 'seat__number']
