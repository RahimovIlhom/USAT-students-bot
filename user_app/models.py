from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import ForeignKey, OneToOneField

EDU_LANGUAGES = (
    ('uz', _('Uzbek')),
    ('ru', _('Russian')),
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
    edu_direction = ForeignKey('education_app.EduDirection', on_delete=models.DO_NOTHING, related_name='students',
                               verbose_name=_('Ta’lim yo‘nalishi'))
    edu_type = ForeignKey('education_app.EduType', on_delete=models.DO_NOTHING, related_name='students',
                          verbose_name=_('Ta’lim turi'))
    edu_lang = models.CharField(max_length=2, choices=EDU_LANGUAGES, default='uz', verbose_name=_('Ta’lim tili'))
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


REGISTER_STATUS = (
    ('DRAFT', _('Qoralama')),
    ('PHONE_INPUT', _('Telefon raqamini kiritish')),
    ('PASSPORT_INPUT', _('Pasport maʼlumotlarini kiritish')),
    ('CONFIRMATION', _('Tasdiqlash kutilmoqda')),
    ('EDIT', _('Tahrirlash')),
    ('COMPLETED', _('Tugatildi')),
    ('BLOCKED', _('Bloklangan')),
)

class User(models.Model):
    tg_id = models.CharField(max_length=20, primary_key=True, verbose_name=_('Telegram ID'))
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Telefon raqami'))
    student = OneToOneField('user_app.Student', null=True, blank=True, on_delete=models.SET_NULL,
                            related_name='user', verbose_name=_('Talaba'))
    chat_lang = models.CharField(max_length=2, choices=EDU_LANGUAGES, null=True, blank=True, verbose_name=_('Chat tili'))
    status = models.CharField(max_length=15, choices=REGISTER_STATUS, default='DRAFT', verbose_name=_('Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Oxirgi yangilangan vaqti'))

    def __str__(self):
        return f"{self.student.fullname} - {self.phone}"

    class Meta:
        indexes = [
            models.Index(fields=['tg_id']),
        ]
        db_table = 'users'
        verbose_name = _('Talaba profil ')
        verbose_name_plural = _('Talaba profillari')
