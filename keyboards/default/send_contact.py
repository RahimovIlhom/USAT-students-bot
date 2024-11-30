from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def contact_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text="📞 Telefon raqamni yuborish" if lang == 'uz' else "📞 Отправить номер телефона",
            request_contact=True
        )
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
