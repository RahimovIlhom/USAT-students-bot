from aiogram.filters.callback_data import CallbackData
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

class CourseNumberCallbackData(CallbackData, prefix='course_number'):
    course_number: int


async def make_callback_data(course_number: int) -> str:
    return CourseNumberCallbackData(course_number=course_number).pack()

async def get_courses_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(len(courses[lang])):
        builder.row(
            InlineKeyboardButton(
                text=courses[lang][i],
                callback_data=await make_callback_data(i+1)
            )
        )
    return builder.as_markup()
