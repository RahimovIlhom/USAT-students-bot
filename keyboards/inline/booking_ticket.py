import emoji
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class BookingTicketCallbackData(CallbackData, prefix="booking_ticket"):
    event_id: int


async def make_callback_data(event_id: int) -> str:
    return BookingTicketCallbackData(event_id=event_id).pack()

booking_ticket_texts = {
    'uz': "Chipta bron qilish",
    'ru': "Забронировать билет"
}


async def booking_ticket_keyboard(lang: str, event_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{emoji.emojize(':ticket:')} {booking_ticket_texts[lang]}",
                    callback_data=await make_callback_data(event_id=event_id)
                )
            ]
        ]
    )
