from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

user_menu_buttons_texts = {
    'uz': [
        "🎟 Taklifnoma olish"
    ],
    'ru': [
        "🎟 Получить предложение"
    ]
}


async def user_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for button_text in user_menu_buttons_texts[lang]:
        builder.row(KeyboardButton(text=button_text))
    return builder.as_markup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
