from django.db import models
from django.utils.translation import gettext_lazy as _


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Hall(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Zal nomi"))
    capacity = models.PositiveIntegerField(verbose_name=_("Sig'imi"))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Manzili"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Tavsif"))
    image = models.ImageField(upload_to='hall_images/', null=True, blank=True, verbose_name=_("Rasm"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktikligi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Oxirgi yangilangan vaqti"))

    # active_objects = ActiveManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}: {self.capacity} sig'imli"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.is_active = False
    #     self.save()

    class Meta:
        verbose_name = _("Zal ")
        verbose_name_plural = _("Zallar")
        db_table = "halls"


class Sector(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='sector_set', verbose_name=_("Zal"))
    name = models.CharField(max_length=100, verbose_name=_("Sektor nomi"))
    # Qatorlar va bo'limlar sonini saqlash
    section_count = models.PositiveIntegerField(default=0, verbose_name="Bo'limlar soni")
    line_count = models.PositiveIntegerField(default=0, verbose_name="Qatorlar soni")
    is_active = models.BooleanField(default=True, verbose_name=_("Aktikligi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Oxirgi yangilangan vaqti"))

    # active_objects = ActiveManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.name} sektor"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True

        # Dastlabki saqlash, pk qiymatini olish uchun
        super().save(*args, **kwargs)

        # Eski Line va Section obyektlarini o'chirish (agar kerak bo'lsa)
        if self.pk:
            # Yangi line_count va section_count bo'yicha eski obyektlarni o'chirish
            current_lines = self.line_set.all()
            current_sections = self.section_set.all()

            # Qatorlarni o'chirish
            if len(current_lines) > self.line_count:
                for line in current_lines[self.line_count:]:
                    line.delete()

            # Bo'limlarni o'chirish
            if len(current_sections) > self.section_count:
                for section in current_sections[self.section_count:]:
                    section.delete()

        # Line va Section obyektlarini yaratish (agar kerak bo'lsa)
        if self.line_count > 0:
            for i in range(self.line_count):
                if i >= len(self.line_set.all()):  # Yangi Line yaratish
                    Line.objects.create(sector=self, number=i + 1)

        if self.section_count > 0:
            for i in range(self.section_count):
                if i >= len(self.section_set.all()):  # Yangi Section yaratish
                    Section.objects.create(sector=self, number=i + 1)

    # def delete(self, *args, **kwargs):
    #     self.is_active = False
    #     self.save()

    class Meta:
        verbose_name = _("Sektor ")
        verbose_name_plural = _("Sektorlar")
        db_table = "sectors"


class Line(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='line_set', verbose_name=_("Sektori"))
    number = models.PositiveIntegerField(verbose_name=_("Qator raqami"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktikligi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Oxirgi yangilangan vaqti"))

    # active_objects = ActiveManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.sector.name} sektor, {self.number}-qator"

    def create_seats(self, start_seat, end_seat, section=None):
        for number in range(start_seat, end_seat + 1):
            Seat.objects.create(line=self, section=section, number=number)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.is_active = False
    #     self.save()

    class Meta:
        verbose_name = _("Qator ")
        verbose_name_plural = _("Qatorlar")
        db_table = "lines"
        ordering = ['sector__name', 'number']


class Section(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='section_set', verbose_name=_("Sektori"))
    number = models.PositiveIntegerField(verbose_name=_("Bo'lim raqami"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktikligi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Oxirgi yangilangan vaqti"))

    # active_objects = ActiveManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.sector.name} sektor, {self.number}-bo'lim"

    def create_seats_in_section(self, start_seat, end_seat, line):
        # O'rindiqlarni yaratish
        for seat_number in range(start_seat, end_seat + 1):
            Seat.objects.create(
                number=seat_number,
                line=line,
                section=self
            )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.is_active = False
    #     self.save()

    class Meta:
        verbose_name = _("Bo'lim ")
        verbose_name_plural = _("Bo'limlar")
        db_table = "sections"
        ordering = ['sector__name', 'number']


class Seat(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE, verbose_name=_("Qatori"))
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Bo'limi"))
    number = models.PositiveIntegerField(verbose_name=_("O'rindiq raqami"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktikligi"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Oxirgi yangilangan vaqti"))

    # active_objects = ActiveManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.line.sector.name} sektor, {self.line.number}-qator, {self.section.number}-bo'lim, {self.number}-joy"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.is_active = False
    #     self.save()

    class Meta:
        verbose_name = _("O‘rindiq ")
        verbose_name_plural = _("O‘rindiqlar")
        db_table = "seats"
        ordering = ['line__sector__name', 'line__number', 'section__number', 'number']
