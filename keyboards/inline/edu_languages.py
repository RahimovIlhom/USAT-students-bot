from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class EduLanguagesCallbackData(CallbackData, prefix='edu_languages'):
    lang: str


async def make_callback_data(lang: str) -> str:
    return EduLanguagesCallbackData(lang=lang).pack()


async def get_edu_languages_keyboard(lang: str) -> InlineKeyboardMarkup:
    texts = {
        'uz': ["🇺🇿 O‘zbek tili", "🇷🇺 Rus tili"],
        'ru': ["🇺🇿 Узбекский", "🇷🇺 Русский"]
    }
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=texts[lang][0], callback_data=await make_callback_data(lang='uz')),
        InlineKeyboardButton(text=texts[lang][1], callback_data=await make_callback_data(lang='ru'))
    )
    return builder.as_markup()
