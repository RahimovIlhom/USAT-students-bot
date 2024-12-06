import emoji
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class BookingTicketCallbackData(CallbackData, prefix="booking_ticket"):
    event_id: int
    user_id: int


async def make_callback_data(event_id: int, user_id: int) -> str:
    return BookingTicketCallbackData(event_id=event_id, user_id=user_id).pack()


async def booking_ticket_keyboard(lang: str, event_id: int, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{emoji.emojize(':ticket:')} {'Buyurtma berish' if lang == 'uz' else 'Сделать заказ'}",
                    callback_data=await make_callback_data(event_id=event_id, user_id=user_id)
                )
            ]
        ]
    )
