from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _


class Ticket(models.Model):
    user = models.ForeignKey('user_app.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Foydalanuvchi'))
    seat = models.ForeignKey('hall_app.Seat', on_delete=models.CASCADE, verbose_name=_('O‘rindiq'))
    event = models.ForeignKey('event_app.Event', on_delete=models.CASCADE, verbose_name=_('Tadbir'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Tadbir narxi"))
    is_paid = models.BooleanField(default=False, verbose_name=_("To‘landimi?"))
    is_booking = models.BooleanField(default=False, verbose_name=_("Bron qilinganmi?"))
    booking_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Bron qilingan vaqti"))
    image = models.ImageField(upload_to='ticket_images/', null=True, blank=True, verbose_name=_("Chipta rasmi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo‘shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Oxirgi yangilangan vaqti'))

    def save(self, *args, **kwargs):
        # Admin tomonidan is_booking false bo'lsa, booking_at va user ni None qilib qo'yish
        if not self.is_booking:
            self.booking_at = None
            self.user = None

        super().save(*args, **kwargs)

    def release_booking_if_expired(self):
        """Bron qilingan vaqti ticket_booking_time dan oshgan bo'lsa, bronni ochadi."""
        if self.is_booking and self.booking_at:
            if now() > self.booking_at + self.event.ticket_booking_time:
                self.is_booking = False
                self.booking_at = None
                self.user = None
                self.save()

    def __str__(self):
        user_name = self.user.student.fullname if self.user else "Foydalanuvchi yo'q"
        return f"{user_name} - {self.event}: {self.seat}"

    class Meta:
        verbose_name = _("Chipta ")
        verbose_name_plural = _("Chiptalar")
        db_table = "tickets"
        ordering = ['-is_booking', '-booking_at', 'event__date', 'seat__line__sector__name', 'seat__line__number', 'seat__section__number', 'seat__number']
