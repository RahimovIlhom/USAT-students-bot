from celery import shared_task
from .models import Event

@shared_task
def update_event_status():
    """Tadbirlarni vaqti bo'yicha statusini yangilash."""
    events = Event.objects.filter(is_active=True)
    for event in events:
        event.update_status()
        event.save()
