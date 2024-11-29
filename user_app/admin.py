from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'passport', 'pinfl', 'course', 'edu_lang', 'edu_direction', 'edu_type')
    list_display_links = ('id', 'fullname')
    list_filter = ('edu_direction', 'edu_type')
    search_fields = ('fullname', 'passport', 'pinfl')
    list_per_page = 10
    save_on_top = True
