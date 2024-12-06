import emoji

from aiogram import F
from aiogram.types import Message, CallbackQuery

from filters.private_filters import PrivateFilter
from keyboards.default import user_menu_buttons_texts
from keyboards.inline import booking_ticket_keyboard, BookingTicketCallbackData, booking_ticket_texts
from loader import dp, db, redis_client, messages
from utils import get_tashkent_timezone


@dp.message(PrivateFilter(), F.text.in_(user_menu_buttons_texts['uz'][0] + user_menu_buttons_texts['ru'][0]))
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
            )
        available_tickets_count = await db.get_available_tickets_count(event['id'])
        if available_tickets_count == 0:
            text += (await messages.get_message(chat_lang, 'no_tickets')).format(name=event[f'name_{chat_lang}'])
            markup = None
        else:
            text += (await messages.get_message(chat_lang, 'yes_tickets')).format(
                    ticket=emoji.emojize(':ticket:'),
                    button=booking_ticket_texts[chat_lang],
                    count=available_tickets_count
                )
            markup = await booking_ticket_keyboard(chat_lang, event['id'], int(message.from_user.id)),
        await message.answer(
            text=text,
            reply_markup=markup,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    else:
        await message.answer(await messages.get_message(chat_lang, 'no_events'), parse_mode="Markdown")


@dp.callback_query(BookingTicketCallbackData.filter())
async def buy_ticket(callback_query: CallbackQuery, callback_data: BookingTicketCallbackData):
    event_id = callback_data.event_id
    user_id = callback_data.user_id
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)

    await db.buy_ticket(event_id, user_id)
    # await callback_query.message.delete()
    # await callback_query.message.answer(await messages.get_message(chat_lang, 'ticket_purchased'),
    #                                     reply_markup=await user_menu(chat_lang))
