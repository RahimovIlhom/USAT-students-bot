from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def check_subscribe_keyboard(chat_lang: str = 'uz') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="✅ Obunani tekshirish" if chat_lang == 'uz' else "✅ Проверить подписку",
            callback_data='check_subscribe'
        )
    )

    return builder.as_markup()
