from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.config import PRIVATE_CHANNEL_LINK


async def subscribe_keyboard(chat_lang: str = 'uz') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="🔗 Kanalga obuna bo'lish" if chat_lang == 'uz' else "🔗 Подписаться на канал",
            url=PRIVATE_CHANNEL_LINK
        )
    )

    return builder.as_markup()
