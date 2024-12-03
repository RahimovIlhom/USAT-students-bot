from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


class EduDirectionCallbackData(CallbackData, prefix="edu_direction"):
    edu_direction_id: int


async def make_callback_data(edu_direction_id: int) -> str:
    return EduDirectionCallbackData(edu_direction_id=edu_direction_id).pack()


async def get_edu_directions_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    directions = await db.get_edu_directions()

    for direction in directions:
        builder.row(
            InlineKeyboardButton(
                text=direction[f"name_{lang}"],
                callback_data=await make_callback_data(edu_direction_id=direction['id'])
            )
        )
    return builder.as_markup()
