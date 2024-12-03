from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


class EduTypeCallbackData(CallbackData, prefix="edu_type"):
    edu_type_id: int


async def make_callback_data(edu_type_id: int) -> str:
    return EduTypeCallbackData(edu_type_id=edu_type_id).pack()


async def get_edu_types_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    edu_types = await db.get_edu_types()

    for edu_type in edu_types:
        builder.row(
            InlineKeyboardButton(
                text=edu_type[f"name_{lang}"],
                callback_data=await make_callback_data(edu_type['id'])
            )
        )
    return builder.as_markup()
