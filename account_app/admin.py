from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # UserAdmin fieldsetsdan foydalanib, qo'shimcha maydonlarni qo'shish
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('phone', 'image', 'about', 'company', 'job')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Add qilish uchun qo'shimcha maydonlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone', 'image', 'about', 'company', 'job')}
        ),
    )

    # Admin panelda qanday maydonlarni ko'rsatish kerakligini aniqlash
    list_display = ('username', 'email', 'is_staff', 'phone', 'company')
    search_fields = ('username', 'email', 'phone')
    filter_horizontal = ('groups', 'user_permissions')


# Django admin ga CustomUserAdmin klassini qo'shamiz
admin.site.register(CustomUser, CustomUserAdmin)
