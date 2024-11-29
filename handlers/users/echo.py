from aiogram import types
from aiogram.enums import ContentType
from aiogram.fsm.state import State

from loader import dp


# Echo bot
@dp.message(State(), lambda msg: msg.content_type == ContentType.TEXT)
async def bot_echo(message: types.Message):
    await message.answer(message.text)
