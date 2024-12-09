from celery import shared_task
import asyncio  # Asinxron funksiyalarni ishlatish uchun

from utils import create_ticket_image  # create_ticket_image - asinxron funksiya

@shared_task
def generate_ticket_image(tg_id, event_id, fullname, ticket_id):
    from ticket_app.models import Ticket

    # Asinxron funksiyani sinxron chaqirish
    ticket_image = asyncio.run(create_ticket_image(tg_id, event_id, fullname))

    # Ticket ma'lumotini yangilash
    Ticket.objects.filter(id=ticket_id).update(image=ticket_image)
