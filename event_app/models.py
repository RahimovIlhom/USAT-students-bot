from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from hall_app.models import Hall, Seat
from ticket_app.models import Ticket

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
    default_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Tadbir narxi"))
    status = models.CharField(max_length=10, choices=EVENT_STATUS, default='no_started', verbose_name=_("Tadbir holati"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktikligi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo‘shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Oxirgi yangilangan vaqti"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Statusni yangilash
        self.update_status()

        # Event saqlanishdan oldin Ticket yaratish
        if not self.pk:  # Agar tadbir yangi bo'lsa
            self.create_tickets_for_seats()
        else:
            # O'rindiqlarni yangilash
            self.update_tickets_for_seats()

            # Tadbir narxi o'zgarganini tekshirish
            old_event = Event.objects.get(pk=self.pk)
            if old_event.default_price != self.default_price:
                self.update_ticket_prices()

        super().save(*args, **kwargs)

    def update_status(self):
        """
        Tadbirni vaqti bo'yicha avtomatik ravishda yangilaydi:
        - Agar tadbir boshlanishi vaqti kelgan bo'lsa, statusni "started" ga o'zgartiradi.
        - Agar tadbir boshlanganidan 2 soat o'tgan bo'lsa, statusni "finished" ga o'zgartiradi.
        """
        if self.date <= now() and self.status == 'no_started':
            self.status = 'started'
        elif self.date <= now() and self.status == 'started' and self.date + timedelta(hours=2) <= now():
            self.status = 'finished'
            self.is_active = False

    def create_tickets_for_seats(self):
        """
        Tadbir uchun zaldagi barcha o'rindiqlar bo'yicha Ticket ob'ektlarini yaratadi.
        """
        seats = Seat.objects.filter(line__sector__hall=self.hall, is_active=True)

        # Faqat Event saqlanmagan bo'lsa, Ticket yaratish
        if not self.pk:  # Agar tadbir yangi bo'lsa
            super().save()  # Eventni saqlash

        for seat in seats:
            # Create a ticket for each seat
            Ticket.objects.get_or_create(
                event=self,
                seat=seat,
                price=self.default_price
            )

    def update_tickets_for_seats(self):
        """
        Tadbir uchun yangi qo'shilgan o'rindiqlar uchun Ticket ob'ektlarini yaratadi.
        """
        existing_seats = Ticket.objects.filter(event=self).values_list('seat', flat=True)
        seats = Seat.objects.filter(line__sector__hall=self.hall, is_active=True)

        # O'rindiqlarni tekshirish va yangilash
        for seat in seats:
            if seat.id not in existing_seats:
                Ticket.objects.get_or_create(
                    event=self,
                    seat=seat,
                    price=self.default_price
                )

    def update_ticket_prices(self):
        """
        Tadbir narxi o'zgarganida barcha tegishli Ticket ob'ektlarini yangilaydi.
        """
        tickets = Ticket.objects.filter(event=self)
        for ticket in tickets:
            ticket.price = self.default_price
            ticket.save()

    class Meta:
        verbose_name = _("Tadbir ")
        verbose_name_plural = _("Tadbirlar")
        db_table = "events"
        ordering = ['-date']
