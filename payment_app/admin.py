from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'method', 'amount', 'status', 'paid_at', 'created_at')
    list_filter = ('method', 'status', 'created_at')
    search_fields = ('transaction_id', 'ticket__id')
    readonly_fields = ('paid_at', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('ticket', 'method', 'amount', 'transaction_id', 'status', 'details')
        }),
        ('Dates', {
            'fields': ('paid_at', 'created_at', 'updated_at')
        }),
    )
