import os

import django
from aiogram.types import CallbackQuery

from keyboards.inline import DownloadBookingCallbackData
from loader import dp, redis_client, db, messages


# Callback handler
@dp.callback_query(DownloadBookingCallbackData.filter())
async def download_ticket(callback_query: CallbackQuery, callback_data: DownloadBookingCallbackData):
    # Reply markup ni o'chirish
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # Ticket ID dan ma'lumot olish
    ticket_id = callback_data.ticket_id
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)

    # DB dan chiptani tekshirish
    ticket = await db.get_ticket(ticket_id, callback_query.from_user.id)

    # Ticket topilmagan yoki to'lanmagan holatlarini tekshirish
    if not ticket:
        await callback_query.answer(await messages.get_message(chat_lang, 'ticket_not_found'), show_alert=True)
        return

    if not ticket['ticket_is_paid']:
        await callback_query.answer(await messages.get_message(chat_lang, 'ticket_unpaid'), show_alert=True)
        return

    # Ticket uchun rasm URL hosil qilish yoki yaratish
    image = ticket['ticket_image']

    if not image:
        await callback_query.answer(await messages.get_message(chat_lang, 'ticket_image_not_found'), show_alert=True)
        return
    image_url = await handle_ticket_image(ticket['ticket_image'])

    # Rasm yuborish
    try:
        await callback_query.message.answer_photo(
            photo=image_url,
            disable_web_page_preview=True
        )
    except Exception as e:
        await callback_query.answer(f"{e}", show_alert=True)


async def handle_ticket_image(ticket_image: str) -> str:
    """
    Ticket uchun tasvir yo'q bo'lsa, yaratish va URL hosil qilish.
    """
    return await get_image_url(ticket_image)


# Django muhitini ishga tushirish
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.conf import settings


async def get_image_url(image_path: str) -> str:
    """
    Yaratilgan yoki mavjud bo'lgan rasm uchun URL hosil qiladi.
    """
    # Tasvirning to'liq URL hosil qilinishi
    return f"{settings.SITE_URL}{settings.MEDIA_URL}{image_path}"
