from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def user_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text="🎟 Taklifnoma olish" if lang == 'uz' else "🎟 Получить предложение"
        )
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
