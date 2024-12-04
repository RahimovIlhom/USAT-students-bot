from django import forms
from django.utils.translation import gettext_lazy as _

from hall_app.models import Section


class SectorForm(forms.ModelForm):
    sections_count = forms.IntegerField(label=_("Bo'limlar soni"), min_value=1, required=True)
    lines_count = forms.IntegerField(label=_("Qatorlar soni"), min_value=1, required=True)

    class Meta:
        model = Section
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:  # Agar zal mavjud bo'lsa
            self.fields['sections_count'].disabled = True
            self.fields['sections_count'].help_text = _("Bu maydon faqat yaratishda ko'rsatiladi")
            self.fields['lines_count'].disabled = True
            self.fields['lines_count'].help_text = _("Bu maydon faqat yaratishda ko'rsatiladi")
        else:
            self.fields['sections_count'].help_text = _("Sektorlar sonini kiriting")
            self.fields['lines_count'].help_text = _("Qatorlar sonini kiriting")