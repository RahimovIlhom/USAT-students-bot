from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'hall', 'date', 'default_price', 'status', 'is_active')
    list_filter = ('status', 'is_active', 'hall', 'date')
    search_fields = ('name', 'description', 'hall__name')
    list_editable = ('status', 'is_active', 'default_price')
    readonly_fields = ('is_active', 'created_at', 'updated_at')
    list_per_page = 10

    # Event holati va vaqti bo'yicha qo'shimcha funksiyalar
    def get_readonly_fields(self, request, obj=None):
        # Tadbirning holati faqat ko'rish uchun
        if obj:
            return ['status', 'is_active']
        return []

    # Event haqida to'liq ma'lumotni ko'rsatish
    def event_display(self, obj):
        return obj.name

    event_display.short_description = "Tadbir nomi"

    # Event holatini avtomatik yangilash
    def update_status_display(self, obj):
        return obj.get_status_display()

    update_status_display.short_description = "Tadbir holati"

    # Eventning statusini va holatini ko'rsatish
    list_display += ('update_status_display',)

admin.site.register(Event, EventAdmin)
