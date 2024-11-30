from django.contrib import admin

from .models import Student, User


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'passport', 'pinfl', 'course', 'edu_lang', 'edu_direction', 'edu_type')
    list_display_links = ('id', 'fullname')
    list_filter = ('edu_direction', 'edu_type')
    search_fields = ('fullname', 'passport', 'pinfl')
    list_per_page = 20


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'phone', 'student', 'status', 'created_at')
    list_display_links = ('tg_id', 'phone', 'student')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('tg_id', 'phone')
    list_per_page = 20
