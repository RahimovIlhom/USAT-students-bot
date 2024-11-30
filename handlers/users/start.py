from aiogram import types
from aiogram.filters import CommandStart

from filters.private_filters import PrivateFilter, PrivateAdminFilter
from keyboards.default import choose_language_keyboard
from loader import dp, messages


@dp.message(PrivateAdminFilter(), CommandStart())
async def admin_bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")


@dp.message(PrivateFilter(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(await messages.get_message('uz', 'welcome'))
    await message.answer(await messages.get_message('uz', 'choose_language'), reply_markup=choose_language_keyboard)
