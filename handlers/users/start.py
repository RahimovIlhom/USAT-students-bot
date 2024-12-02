from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from filters.private_filters import PrivateFilter, PrivateAdminFilter
from handlers.users.register import confirmation
from keyboards.default import choose_language_keyboard, contact_keyboard, user_menu
from keyboards.inline import edit_student_data_keyboard
from loader import dp, messages, redis_client, db
from states import RegisterForm


@dp.message(PrivateAdminFilter(), CommandStart())
async def admin_bot_start(message: types.Message):
    await message.answer(f"Admin panel")


@dp.message(PrivateFilter(), CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chat_lang = await redis_client.get_user_chat_lang(user_id) or 'uz'

    user_status = await redis_client.get_user_status(user_id)

    status_messages = {
        'DRAFT': ('choose_language', choose_language_keyboard, RegisterForm.chat_lang),
        'PHONE_INPUT': ('phone_input', await contact_keyboard(chat_lang), RegisterForm.phone),
        'PASSPORT_INPUT': ('passport_input', ReplyKeyboardRemove(), RegisterForm.passport),
        'EDIT': ('edit', await edit_student_data_keyboard(chat_lang), RegisterForm.edit_fullname),
        'BLOCKED': ('blocked', ReplyKeyboardRemove(), None),
    }

    if not user_status:
        await redis_client.set_user_status(user_id, 'DRAFT')
        await db.add_draft_user(user_id, 'DRAFT')
        await message.answer(await messages.get_message(chat_lang, 'welcome'))
        await state.set_state(RegisterForm.chat_lang)
        user_status = "DRAFT"

    # Handle user status based on current status
    if user_status == "CONFIRMATION":
        student = await db.get_student(await redis_client.get_user_passport(user_id))
        await confirmation(message, chat_lang, student, state)
        return

    # Lookup message, keyboard, and next state for the user's status
    status_data = status_messages.get(user_status)

    if not status_data:
        await message.answer(await messages.get_message(chat_lang, 'restart'),
                             reply_markup=await user_menu(chat_lang))
        await state.clear()
        return

    # Unpack message key, keyboard, and next state
    message_key, keyboard, next_state = status_data
    await message.answer(await messages.get_message(chat_lang, message_key), reply_markup=keyboard)

    # Set the next state if applicable
    if next_state:
        await state.set_state(next_state)

