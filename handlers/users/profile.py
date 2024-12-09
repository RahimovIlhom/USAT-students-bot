from aiogram import F
from aiogram.types import Message

from filters.private_filters import PrivateFilter
from keyboards.default import user_menu_buttons_texts
from loader import dp, redis_client, messages


@dp.message(PrivateFilter(), F.text.in_(user_menu_buttons_texts['uz'][2] + user_menu_buttons_texts['ru'][2]))
async def settings(message: Message):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await message.answer(await messages.get_message('uz', 'settings'), )