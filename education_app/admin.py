from django.contrib import admin

from .models import EduDirection, EduType

@admin.register(EduDirection)
class EduDirectionAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru')
    list_display_links = ('name_uz', 'name_ru')
    search_fields = ('name_uz', 'name_ru')
    list_filter = ('name_uz', 'name_ru')

@admin.register(EduType)
class EduTypeAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru')
    list_display_links = ('name_uz', 'name_ru')
    search_fields = ('name_uz', 'name_ru')
    list_filter = ('name_uz', 'name_ru')
