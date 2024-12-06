from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    # Tadbir va o'rindiq bilan bog'lanishni qo'shish
    list_display = ('event', 'user', 'seat', 'price', 'is_paid', 'is_booking')
    list_filter = ('event', 'seat__line__sector__hall', 'is_paid', 'is_booking', 'created_at')
    search_fields = ('event__name', 'seat__id')
    list_editable = ('price', 'is_paid', 'is_booking')
    list_per_page = 40

    # O'rindiqlar va Tadbirlar bilan bog'lanishni qo'shish
    def get_readonly_fields(self, request, obj=None):
        # Tadbir va o'rindiq faqat ko'rish uchun bo'lishi kerak
        if obj:  # Agar ob'ekt mavjud bo'lsa
            return ['event', 'seat']
        return []

admin.site.register(Ticket, TicketAdmin)
