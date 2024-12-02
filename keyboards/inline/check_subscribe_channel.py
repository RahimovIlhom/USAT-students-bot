from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def check_subscribe_keyboard(channels: List[dict], chat_lang: str = 'uz') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for channel in channels:
        builder.row(
            InlineKeyboardButton(
                text=channel['title'],
                url=channel['link']
            )
        )

    builder.row(
        InlineKeyboardButton(
            text="✅ Obunani tekshirish" if chat_lang == 'uz' else "✅ Проверить подписку",
            callback_data='check_subscribe'
        )
    )

    return builder.as_markup()
