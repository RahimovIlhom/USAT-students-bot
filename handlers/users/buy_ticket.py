import emoji

from aiogram import F
from aiogram.types import Message, CallbackQuery

from filters.private_filters import PrivateFilter
from keyboards.default import user_menu_buttons_texts
from keyboards.inline import booking_ticket_keyboard, BookingTicketCallbackData
from loader import dp, db, redis_client, messages
from utils import get_tashkent_timezone


@dp.message(PrivateFilter(), F.text.in_(user_menu_buttons_texts['uz'] + user_menu_buttons_texts['ru']))
async def buy_ticket(message: Message):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    event = await db.get_next_upcoming_event()

    if event:
        available_tickets_count = await db.get_available_tickets_count(event['id'])
        if available_tickets_count == 0:
            await message.answer(
                (await messages.get_message(chat_lang, 'no_tickets')).format(name=event[f'name_{chat_lang}']),
                parse_mode="Markdown"
            )
            return
        await message.answer((await messages.get_message(chat_lang, 'next_event')).format(
                emoji=emoji.emojize(':sparkles:'),
                name=event[f'name_{chat_lang}'],
                body=event.get(f'description_{chat_lang}') or '',
                date=(await get_tashkent_timezone(date=event['date'])).strftime('%d-%m-%Y %H:%M'),
                price=event['default_price'],
                ticket=emoji.emojize(':ticket:'),
                count=available_tickets_count
            ),
            reply_markup=await booking_ticket_keyboard(chat_lang, event['id'], int(message.from_user.id)),
            parse_mode="Markdown"
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
