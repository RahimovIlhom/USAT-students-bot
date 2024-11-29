from modeltranslation.translator import register, TranslationOptions

from .models import EduDirection, EduType


@register(EduDirection)
class EduDirectionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(EduType)
class EduTypeTranslationOptions(TranslationOptions):
    fields = ('name',)