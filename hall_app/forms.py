from django import forms
from django.utils.translation import gettext_lazy as _

from hall_app.models import Section, Line


# Custom forma
class SeatCreationForm(forms.Form):
    start_seat = forms.IntegerField(label=_("Boshlanish o‘rindiq raqami"), min_value=1)
    end_seat = forms.IntegerField(label=_("Tugash o‘rindiq raqami"), min_value=1)
    section = forms.ModelChoiceField(
        queryset=Section.objects.none(),
        required=False,
        label="Bo'lim (ixtiyoriy)"
    )

    def __init__(self, *args, line=None, **kwargs):
        super().__init__(*args, **kwargs)
        if line:
            self.fields['section'].queryset = Section.objects.filter(is_active=True, sector=line.sector)


class SectionSeatCreationForm(forms.Form):
    start_seat = forms.IntegerField(label=_("Boshlanish o‘rindiq raqami"), min_value=1, required=True)
    end_seat = forms.IntegerField(label=_("Tugash o‘rindiq raqami"), min_value=1, required=True)
    line = forms.ModelChoiceField(queryset=Line.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        section = kwargs.pop('section', None)
        super().__init__(*args, **kwargs)
        self.fields['section'] = forms.ModelChoiceField(queryset=Section.objects.filter(id=section.id), required=True)

    class Meta:
        fields = ['start_seat', 'end_seat', 'line', 'section']