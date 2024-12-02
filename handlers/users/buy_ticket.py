from aiogram import F
from aiogram.types import Message

from filters.private_filters import PrivateFilter
from loader import dp


@dp.message(PrivateFilter(), F.text == "🎟 Taklifnoma olish")
async def buy_ticket(message: Message):
    await message.answer("Buy ticket")


@dp.message(PrivateFilter(), F.text == "🎟 Получить предложение")
async def buy_ticket(message: Message):
    await message.answer("Buy ticket")
