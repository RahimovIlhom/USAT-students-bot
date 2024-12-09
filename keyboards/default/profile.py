from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

profile_buttons_texts = {
    'uz': [
        "📋 Ma’lumotlarim",
        "🎫 Mening chiptam",
        "🔙 Orqaga"
    ],
    'ru': [
        "📋 Мои данные",
        "🎫 Мой билет",
        "🔙 Назад"
    ]
}


async def profile_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for button_text in profile_buttons_texts[lang]:
        builder.add(KeyboardButton(text=button_text))
    builder.adjust(2, 1)
    return builder.as_markup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
