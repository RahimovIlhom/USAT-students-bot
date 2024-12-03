from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

user_menu_buttons_texts = {
    'uz': [
        "🎫 Tadbirga chipta sotib olish",
        "⚙️ Sozlamalar",
        "👤 Profilim",
    ],
    'ru': [
        "🎫 Купить билет на мероприятие",
        "⚙️ Настройки",
        "👤 Профиль",
    ]
}


async def user_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for button_text in user_menu_buttons_texts[lang]:
        builder.add(KeyboardButton(text=button_text))
    builder.adjust(1, 2)
    return builder.as_markup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
