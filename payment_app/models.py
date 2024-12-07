from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

PAYMENT_METHODS = (
    ('cash', _('Naqd')),
    ('card', _('Karta')),
    ('click', _('Click')),
    ('payme', _('Payme')),
)

PAYMENT_STATUS = (
    ('pending', _('Kutilmoqda')),
    ('completed', _('Bajarildi')),
    ('failed', _('Muvaffaqiyatsiz')),
)


class Payment(models.Model):
    ticket = models.ForeignKey('ticket_app.Ticket', on_delete=models.CASCADE, related_name='payment_set', verbose_name=_('Bilet'))
    method = models.CharField(max_length=5, choices=PAYMENT_METHODS, default='cash', verbose_name=_('To\'lov turi'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('To\'lov summasi'))
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name=_('Tranzaksiya ID'))
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending', verbose_name=_('Holat'))
    details = models.JSONField(null=True, blank=True, verbose_name=_('Qo\'shimcha tafsilotlar'))
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name=_('To\'langan vaqti'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Qo\'shilgan vaqti'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Oxirgi yangilangan vaqti'))

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.paid_at:
            self.paid_at = timezone.now()
            self.ticket.is_paid = True
            self.ticket.save(update_fields=['is_paid'])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket} - {self.amount} ({self.method}: {self.status})"

    class Meta:
        verbose_name = _('To\'lov ')
        verbose_name_plural = _('To\'lovlar')
        db_table = 'payments'
        ordering = ['-created_at']
