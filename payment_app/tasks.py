import aiohttp
from asgiref.sync import async_to_sync
from celery import shared_task
from django.conf import settings

from data.config import SEND_PHOTO_URL, BOT_TOKEN
from utils import create_ticket_image  # create_ticket_image - asinxron funksiya


@shared_task
def generate_ticket_image(tg_id, event_id, fullname, ticket_id):
    from ticket_app.models import Ticket

    # Asinxron funktsiyani sinxron chaqirish
    ticket_image = async_to_sync(create_ticket_image)(tg_id, event_id, fullname)

    # Ticket ma'lumotini yangilash
    Ticket.objects.filter(id=ticket_id).update(image=ticket_image)

    # To'liq URL hosil qilish uchun request yordamida
    full_image_url = f"{settings.SITE_URL}/media/{ticket_image}"

    # Telegram bot orqali rasm yuborish uchun sinxron tarzda chaqirish
    async_to_sync(send_photo)(tg_id, full_image_url)


async def send_photo(chat_id, photo_url):
    """
    Telegram bot API-ga yuboriluvchi rasm URL'sini to'liq manzilga formatlash va yuborish.
    """
    # Yuboriluvchi rasm URL'ini formatlash
    send_photo_url = SEND_PHOTO_URL.format(BOT_TOKEN=BOT_TOKEN, chat_id=chat_id, photo_url=photo_url)

    # Rasm yuborish
    await fetch_url(send_photo_url)


async def fetch_url(url):
    """
    URL manziliga GET request yuborish.
    """
    async with aiohttp.ClientSession() as session:
        try:
            await session.get(url)
        except Exception as e:
            raise Exception(f"Error while trying to send the photo: {e}")
