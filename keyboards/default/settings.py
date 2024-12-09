from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

settings_buttons_texts = {
    'uz': [
        "🌐 Tilni o‘zgartirish",
        "🔙 Orqaga"
    ],
    'ru': [
        "🌐 Изменить язык",
        "🔙 Назад"
    ]
}


async def settings_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for button_text in settings_buttons_texts[lang]:
        builder.add(KeyboardButton(text=button_text))
    builder.adjust(1, 1)
    return builder.as_markup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
