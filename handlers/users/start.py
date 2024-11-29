from aiogram import types
from aiogram.filters import CommandStart

from filters.private_filters import PrivateFilter, PrivateAdminFilter
from loader import dp


@dp.message(PrivateAdminFilter(), CommandStart())
async def admin_bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")


@dp.message(PrivateFilter(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")
