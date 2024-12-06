import emoji

from aiogram import F
from aiogram.types import Message

from filters.private_filters import PrivateFilter
from keyboards.default import user_menu_buttons_texts
from loader import dp, db, redis_client, messages
from utils import get_tashkent_timezone


@dp.message(PrivateFilter(), F.text.in_(user_menu_buttons_texts['uz'] + user_menu_buttons_texts['ru']))
async def buy_ticket(message: Message):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    event = await db.get_next_upcoming_event()

    if event:
        text = (await messages.get_message(chat_lang, 'next_event')).format(
            emoji=emoji.emojize(':sparkles:'),
            name=event[f'name_{chat_lang}'],
            body=event.get(f'description_{chat_lang}') or '',
            date=(await get_tashkent_timezone(date=event['date'])).strftime('%d-%m-%Y %H:%M'),
            price=event['default_price'],
            ticket=emoji.emojize(':ticket:'),
        )
    else:
        text = await messages.get_message(chat_lang, 'no_events')

    # Foydalanuvchiga javob qaytarish
    await message.answer(text, parse_mode="Markdown")
