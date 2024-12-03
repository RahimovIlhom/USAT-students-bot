from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CheckSubscribeCallbackData(CallbackData, prefix='check_subscribe'):
    button_type: str
    data: str
    message: str


async def make_callback_data(button_type: str, data: str, message: str = '') -> str:
    return CheckSubscribeCallbackData(button_type=button_type, data=data, message=message).pack()


async def check_subscribe_keyboard(channels: List[dict], chat_lang: str = 'uz') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for channel in channels:
        if channel['type'] == 'link':
            builder.row(
                    InlineKeyboardButton(
                        text=channel['title'],
                        url=channel['link']
                    )
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text=channel['title'],
                    callback_data=await make_callback_data(
                        button_type=channel['type'],
                        data=channel.get('data', ''),
                        message=channel.get('message', '')
                    )
                )
            )

    builder.row(
        InlineKeyboardButton(
            text="✅ Obunani tekshirish" if chat_lang == 'uz' else "✅ Проверить подписку",
            callback_data=await make_callback_data(button_type='data', data='check_subscribe')
        )
    )

    return builder.as_markup()
