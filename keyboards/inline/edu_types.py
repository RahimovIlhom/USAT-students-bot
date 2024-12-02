from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


async def get_edu_types_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    edu_types = await db.get_edu_types()

    for edu_type in edu_types:
        builder.row(
            InlineKeyboardButton(
                text=edu_type[f"name_{lang}"],
                callback_data=f"{edu_type['id']}"
            )
        )
    return builder.as_markup()
