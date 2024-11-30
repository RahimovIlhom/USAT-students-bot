from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def registration_confirmation_keyboard(chat_lang: str = 'uz') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="✏️ Tahrirlash" if chat_lang == 'uz' else "✏️ Редактировать",
            callback_data='registration_confirmation_edit'
        ),
        InlineKeyboardButton(
            text="✅ Tasdiqlash" if chat_lang == 'uz' else "✅ Подтвердить",
            callback_data='registration_confirm'
        )
    )
    return builder.as_markup()
