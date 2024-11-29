from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import ForeignKey


EDU_LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)

CURRENCY_CHOICES = (
    ('UZS', 'UZS'),
    ('USD', 'USD'),
    ('RUB', 'RUB'),
    ('EUR', 'EUR'),
)


class Student(models.Model):
    fullname = models.CharField(max_length=100, verbose_name=_('Ism familiya'))
    passport = models.CharField(max_length=9, unique=True, verbose_name=_('Passport'))
    pinfl = models.CharField(max_length=14, verbose_name=_('PINFL'))
    course = models.CharField(max_length=1, verbose_name=_('Kurs'))
    edu_direction = ForeignKey('education_app.EduDirection', on_delete=models.DO_NOTHING, verbose_name=_('Ta\'lim yo\'nalishi'))
    edu_type = ForeignKey('education_app.EduType', on_delete=models.DO_NOTHING, verbose_name=_('Ta\'lim turi'))
    edu_lang = models.CharField(max_length=2, choices=EDU_LANGUAGES, default='uz', verbose_name=_('Ta\'lim tili'))
    contract_amount = models.CharField(max_length=10, verbose_name=_('Shartnoma summasi'))
    voucher_amount = models.CharField(max_length=10, verbose_name=_('Voucher summasi'))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UZS', verbose_name=_('Valyuta'))

    def __str__(self):
        return self.fullname

    class Meta:
        indexes = [
            models.Index(fields=['passport']),  # Passport number bo'yicha indeks yaratish
        ]
        db_table = 'students'
        ordering = ['id']
        verbose_name = _('Talaba ')
        verbose_name_plural = _('Talabalar')
