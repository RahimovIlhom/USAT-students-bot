from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def edit_student_data_keyboard(chat_lang: str = 'uz') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Emoji bilan tugmalarni yaratish
    if chat_lang == 'uz':
        builder.row(
            InlineKeyboardButton(
                text="✏️ Ism-familiyani o'zgartirish",
                callback_data='edit_fullname'
            ),
        )
        builder.row(InlineKeyboardButton(
                text="🔢 Kursni o'zgartirish",
                callback_data='edit_course'
            ),
        )
        builder.row(InlineKeyboardButton(
                text="🎓  Ta'lim yo'nalishni o'zgartirish",
                callback_data='edit_edu_direction'
            ),
        )
        builder.row(InlineKeyboardButton(
                text="💡 Ta'lim turi o'zgartirish",
                callback_data='edit_edu_type'
            ),
        )
        builder.row(InlineKeyboardButton(
                text="🌐 Ta'lim tili o'zgartirish",
                callback_data='edit_edu_lang'
            )
        )
    elif chat_lang == 'ru':
        builder.row(
            InlineKeyboardButton(
                text="✏️ Изменить имя и фамилию",
                callback_data='edit_fullname'
            ),
        )
        builder.row(InlineKeyboardButton(
                text="🔢 Изменить курс",
                callback_data='edit_course'
            ),
        )
        builder.row(InlineKeyboardButton(
                text="🎓  Изменить направление обучения",
                callback_data='edit_edu_direction'
            ),
        )
        builder.row(InlineKeyboardButton(
                text="💡 Изменить тип обучения",
                callback_data='edit_edu_type'
            ),
        )
        builder.row(InlineKeyboardButton(
                text="🌐 Изменить язык обучения",
                callback_data='edit_edu_lang'
            )
        )

    return builder.as_markup(row_width=1)
