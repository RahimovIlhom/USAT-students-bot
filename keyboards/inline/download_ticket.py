import emoji
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class DownloadBookingCallbackData(CallbackData, prefix="download_ticket"):
    ticket_id: int


async def make_callback_data(ticket_id: int) -> str:
    return DownloadBookingCallbackData(ticket_id=ticket_id).pack()


download_ticket_texts = {
    'uz': 'Chiptani yuklash',
    'ru': 'Загрузить билет'
}


async def download_ticket_keyboard(lang: str, ticket_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{emoji.emojize(':down_arrow:')} {download_ticket_texts[lang]}",
                    callback_data=await make_callback_data(ticket_id=ticket_id)
                )
            ]
        ]
    )
