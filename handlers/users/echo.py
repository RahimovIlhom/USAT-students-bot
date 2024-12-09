import re

from aiogram import F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from filters.private_filters import PrivateFilter
from handlers.users.register import set_language, set_phone, set_passport, PASSPORT_REGEX, confirmation
from keyboards.default import user_menu
from keyboards.inline import edit_student_data_keyboard
from loader import dp, redis_client, messages, db
from states import RegisterForm


@dp.message(PrivateFilter(), State(), F.text.in_(['🔙 Orqaga', '🔙 Назад']))
async def cancel(message: Message):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await message.answer(await messages.get_message(chat_lang, 'restart'), reply_markup=await user_menu(chat_lang))


async def get_user_data(user_id: int):
    """Retrieve user status and language in one call."""
    user_status = await redis_client.get_user_status(user_id)
    chat_lang = await redis_client.get_user_chat_lang(user_id)
    return user_status, chat_lang

async def handle_draft_state(message: Message, state: FSMContext, *args, **kwargs):
    """Handle the 'DRAFT' state."""
    await state.set_state(RegisterForm.chat_lang)
    await set_language(message, state)

async def handle_passport_input_state(message: Message, state: FSMContext, chat_lang: str):
    """Handle the 'PASSPORT_INPUT' state."""
    await state.set_state(RegisterForm.passport)
    if re.match(PASSPORT_REGEX, message.text):
        await set_passport(message, state)
    else:
        await message.answer(await messages.get_message(chat_lang, 'invalid_passport'),
                             reply_markup=ReplyKeyboardRemove())

async def handle_confirmation_state(message: Message, state: FSMContext, chat_lang: str):
    """Handle the 'CONFIRMATION' state."""
    await message.delete()
    await state.set_state(RegisterForm.confirm)
    passport = await redis_client.get_user_passport(message.from_user.id)
    student = await db.get_student(passport)
    await confirmation(message, chat_lang, student, state)

async def handle_edit_state(message: Message, state: FSMContext, chat_lang: str):
    """Handle the 'EDIT' state."""
    await message.delete()
    await state.set_state(RegisterForm.edit)
    await message.answer(await messages.get_message(chat_lang, 'edit'),
                         reply_markup=await edit_student_data_keyboard(chat_lang))


@dp.message(PrivateFilter(), State(), lambda msg: msg.content_type == ContentType.TEXT)
async def route_message_handler(message: Message, state: FSMContext):
    """Route the message based on user status."""
    user_status, chat_lang = await get_user_data(message.from_user.id)

    state_handlers = {
        "DRAFT": handle_draft_state,
        "PASSPORT_INPUT": handle_passport_input_state,
        "CONFIRMATION": handle_confirmation_state,
        "EDIT": handle_edit_state
    }

    # Check if user status is not "COMPLETED"
    if user_status != "COMPLETED":
        handler = state_handlers.get(user_status)
        if handler:
            await handler(message, state, chat_lang)
    else:
        await message.answer(message.text)


@dp.message(State(), lambda msg: msg.content_type == ContentType.CONTACT)
async def send_contact(message: Message, state: FSMContext):
    user_status = await redis_client.get_user_status(message.from_user.id)
    if user_status == "PHONE_INPUT":
        await state.set_state(RegisterForm.phone)
        await set_phone(message, state)
