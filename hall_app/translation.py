from modeltranslation.translator import register, TranslationOptions

from .models import Hall, Sector


@register(Hall)
class EventTranslationOptions(TranslationOptions):
    fields = ('name', 'address', 'description')


@register(Sector)
class SectorTranslationOptions(TranslationOptions):
    fields = ('name',)
