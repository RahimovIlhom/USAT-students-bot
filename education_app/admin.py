from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import EduDirection, EduType


@admin.register(EduDirection)
class EduDirectionAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )


@admin.register(EduType)
class EduTypeAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )
