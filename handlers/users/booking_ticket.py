from datetime import timedelta

import emoji

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from filters.private_filters import PrivateFilter
from keyboards.default import user_menu_buttons_texts
from keyboards.inline import booking_ticket_keyboard, BookingTicketCallbackData, booking_ticket_texts, \
    download_ticket_keyboard
from loader import dp, db, redis_client, messages
from utils import get_tashkent_timezone


SPARKLES_EMOJI = emoji.emojize(':sparkles:')
TICKET_EMOJI = emoji.emojize(':ticket:')
SUCCESS_EMOJI = emoji.emojize(':white_check_mark:')
MEMO_EMOJI = emoji.emojize(':memo:')
HASH_EMOJI = emoji.emojize(':hash:')
ROUND_PUSHPIN_EMOJI = emoji.emojize(':round_pushpin:')
SEAT_EMOJI = emoji.emojize(':seat:')
CALENDAR_EMOJI = emoji.emojize(':calendar:')
MONEY_BUG_EMOJI = emoji.emojize(':moneybag:')
ARROW_DOWN_EMOJI = emoji.emojize(':arrow_down:')

async def format_remaining_time(lang: str, remaining_time: timedelta) -> str:
    """
    Qolgan vaqti (timedelta obyekti) MM:SS formatida qaytaruvchi funksiya.
    """
    minutes_left = remaining_time.seconds // 60
    seconds_left = remaining_time.seconds % 60

    return (await messages.get_message(lang, 'format_remaining_time')).format(minutes_left=minutes_left, seconds_left=seconds_left)


async def generate_event_message(lang, event, available_tickets_count) -> tuple[str, InlineKeyboardMarkup | None]:
    base_message = (await messages.get_message(lang, 'next_event')).format(
        emoji=SPARKLES_EMOJI,
        name=event[f'name_{lang}'],
        body=event.get(f'description_{lang}') or '',
        date=(await get_tashkent_timezone(event['date'])).strftime('%d-%m-%Y %H:%M'),
        price=event['default_price'],
    )
    if available_tickets_count == 0:
        return base_message + (await messages.get_message(lang, 'no_tickets')).format(name=event[f'name_{lang}']), None
    return base_message + (await messages.get_message(lang, 'yes_tickets')).format(
        ticket=TICKET_EMOJI,
        button=booking_ticket_texts[lang],
        count=available_tickets_count,
        booking_time=await format_remaining_time(lang, event['ticket_booking_time'])
    ), await booking_ticket_keyboard(lang, event['id'])


@dp.message(PrivateFilter(), F.text.in_(user_menu_buttons_texts['uz'][0] + user_menu_buttons_texts['ru'][0]))
async def buy_ticket(message: Message):
    lang = await redis_client.get_user_chat_lang(message.from_user.id)
    event = await db.get_next_upcoming_event()

    if event:
        available_tickets_count = await db.get_available_tickets_count(event['id'])
        text, markup = await generate_event_message(lang, event, available_tickets_count)
    else:
        text = await messages.get_message(lang, 'no_events')
        markup = None

    await message.answer(
        text=text,
        reply_markup=markup,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


async def generate_ticket_message(lang, status, ticket) -> str:
    """Generate a message based on ticket status."""
    if not ticket:
        return await messages.get_message(lang, 'ticket_unavailable')

    # Common data for formatting
    line = ticket.get('line_number', 'N/A')
    seat = ticket.get('seat_number', 'N/A')

    # Helper function to format time safely
    async def format_time(key):
        dt = ticket.get(key)
        if not dt:
            return 'N/A'
        return (await get_tashkent_timezone(dt)).strftime('%d-%m-%Y %H:%M')

    # Prepare message mapping dynamically
    templates = {
        'paid': {
            'template': 'already_paid_ticket',
            'data': {
                'line': line,
                'seat': seat,
                'payment_date': await format_time('payment_paid_at'),
            },
        },
        'unpaid': {
            'template': 'already_booked_ticket',
            'data': {
                'line': line,
                'seat': seat,
                'booking_date': await format_time('ticket_booking_at'),
                'remaining_time': await format_remaining_time(lang, ticket.get('time_remaining', timedelta(0))),
            },
        },
        'booked': {
            'template': 'ticket_booked',
            'data': {
                'line': line,
                'seat': seat,
                'booking_date': await format_time('ticket_booking_at'),
                'remaining_time': await format_remaining_time(lang, ticket.get('time_remaining', timedelta(0))),
            },
        },
        'reload_booking': {
            'template': 'reload_booking_ticket',
            'data': {
                'line': line,
                'seat': seat,
                'booking_date': await format_time('ticket_booking_at'),
                'remaining_time': await format_remaining_time(lang, ticket.get('time_remaining', timedelta(0))),
            },
        },
        'unavailable': {
            'template': 'ticket_unavailable',
            'data': {},
        },
    }

    # Get the template and data for the given status
    message_template = templates.get(status, templates['unavailable'])
    template = await messages.get_message(lang, message_template['template'])
    return template.format(**message_template['data'])


@dp.callback_query(BookingTicketCallbackData.filter())
async def booking_ticket(callback_query: CallbackQuery, callback_data: BookingTicketCallbackData):
    await callback_query.message.edit_reply_markup(reply_markup=None)

    event_id = callback_data.event_id
    user_id = callback_query.from_user.id
    chat_lang = await redis_client.get_user_chat_lang(user_id)

    # Check event status
    active_event = await db.get_active_event(event_id)
    if not active_event:
        await callback_query.answer(await messages.get_message(chat_lang, 'event_finished'), show_alert=True)
        return

    # Check user's ticket booking
    ticket = await db.has_user_booked_ticket(event_id, user_id)
    status, markup = None, None

    if ticket:
        # User has already booked a ticket
        if ticket['ticket_is_paid']:
            status = 'paid'
            markup = await download_ticket_keyboard(chat_lang, ticket['ticket_id'])
        else:
            if ticket['time_remaining'] < timedelta(0):
                await db.booking_ticket(ticket['ticket_id'], user_id)  # Extend booking time
                ticket = await db.has_user_booked_ticket(event_id, user_id)  # Refresh ticket
                status = 'reload_booking'
            else:
                status = 'unpaid'
    else:
        # Check for available unbooked tickets
        ticket = await db.get_first_unbooked_ticket(event_id)
        if ticket:
            status = 'booked'
            await db.booking_ticket(ticket['ticket_id'], user_id)
        else:
            status = 'unavailable'

    # Generate the appropriate message
    text = await generate_ticket_message(chat_lang, status, ticket)

    await callback_query.message.answer(
        text=text,
        reply_markup=markup,
        disable_web_page_preview=True
    )
