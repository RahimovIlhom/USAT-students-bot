from aiogram import F
from aiogram.types import Message

from data.config import PRIVATE_CHANNELS
from filters.private_filters import PrivateFilter
from keyboards.inline import check_subscribe_keyboard
from loader import dp, bot
from utils.misc import check_subscription_channel


@dp.message(PrivateFilter(), F.text == "🎟 Taklifnoma olish")
async def buy_ticket(message: Message):
    channels_format = str()
    for channel_id in PRIVATE_CHANNELS:
        chat = await bot.get_chat(channel_id)
        invite_link = await chat.export_invite_link()
        if not (await check_subscription_channel(message.from_user.id, channel_id)):
            channels_format += f"<a href='{invite_link}'>{chat.title}</a>\n"

    await message.answer(f"Buy ticket\n\n{channels_format}",
                         reply_markup=await check_subscribe_keyboard('uz'), parse_mode="HTML")


@dp.message(PrivateFilter(), F.text == "🎟 Получить предложение")
async def buy_ticket(message: Message):
    await message.answer("Buy ticket")
