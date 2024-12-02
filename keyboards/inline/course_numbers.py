from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder

courses = {
    'uz': [
        '1-kurs',
        '2-kurs',
        '3-kurs',
    ],
    'ru': [
        '1 курс',
        '2 курс',
        '3 курс',
    ]
}

async def get_courses_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(len(courses[lang])):
        builder.row(
            InlineKeyboardButton(
                text=courses[lang][i],
                callback_data=f'{i+1}'
            )
        )
    return builder.as_markup()
