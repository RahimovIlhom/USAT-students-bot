from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


async def get_edu_directions_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    directions = await db.get_edu_directions()

    for direction in directions:
        builder.row(
            InlineKeyboardButton(
                text=direction[f"name_{lang}"],
                callback_data=f"{direction['id']}"
            )
        )
    return builder.as_markup()
