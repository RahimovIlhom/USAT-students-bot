from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿 O‘zbek tili"),
            KeyboardButton(text="🇷🇺 Русский язык")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
