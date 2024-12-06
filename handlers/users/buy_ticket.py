import emoji

from aiogram import F
from aiogram.types import Message

from filters.private_filters import PrivateFilter
from loader import dp, db
from utils import get_tashkent_timezone


@dp.message(PrivateFilter(), F.text.in_(["🎫 Tadbirga chipta sotib olish", "🎫 Купить билет на мероприятие"]))
async def buy_ticket(message: Message):
    event = await db.get_next_upcoming_event()

    if event:
        # Formatlash
        formatted_event_date = (await get_tashkent_timezone(date=event['date'])).strftime('%d-%m-%Y %H:%M')
        text = (
            f"{emoji.emojize(':sparkles:')} **Keyingi Tadbir:** *{event['name']}*\n\n"
            f"{event['description'] if event['description'] else ''}\n"
            f"**Boshlanish vaqti:** {formatted_event_date}\n"
            f"**Chipta narxi:** {event['default_price']} so‘m\n\n"
            f"{emoji.emojize(':ticket:')} *Chipta sotib olish uchun biz bilan bog‘laning!*"
        )
    else:
        text = (
            f"❌ **Ayni paytda yaqinlashib kelayotgan tadbirlar mavjud emas.**\n\n"
            f"*Iltimos, keyinroq yana urinib ko‘ring!*"
        )

    # Foydalanuvchiga javob qaytarish
    await message.answer(text, parse_mode="Markdown")
