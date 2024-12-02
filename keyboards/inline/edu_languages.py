from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_edu_languages_keyboard(lang: str) -> InlineKeyboardMarkup:
    texts = {
        'uz': ["🇺🇿 O'zbek tili", "🇷🇺 Rus tili"],
        'ru': ["🇺🇿 Узбекский", "🇷🇺 Русский"]
    }
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=texts[lang][0], callback_data='uz'),
        InlineKeyboardButton(text=texts[lang][1], callback_data='ru')
    )
    return builder.as_markup()
