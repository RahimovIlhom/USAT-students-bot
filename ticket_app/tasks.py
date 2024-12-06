from celery import shared_task
from ticket_app.models import Ticket


@shared_task
def release_expired_bookings():
    """Bron muddati tugagan barcha biletlarni ochib qo‘yish."""
    tickets = Ticket.objects.filter(is_paid=False, is_booking=True, booking_at__isnull=False)
    for ticket in tickets:
        ticket.release_booking_if_expired()
