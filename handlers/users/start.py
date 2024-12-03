import asyncio

from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from filters.private_filters import PrivateFilter, PrivateAdminFilter
from handlers.users.register import confirmation
from keyboards.default import choose_language_keyboard, contact_keyboard, user_menu
from keyboards.inline import edit_student_data_keyboard, check_subscribe_keyboard
from loader import dp, messages, redis_client, db, bot
from states import RegisterForm
from utils.misc import unsubscribed_channels


@dp.message(PrivateAdminFilter(), CommandStart())
async def admin_bot_start(message: types.Message):
    await message.answer(f"Admin panel")


@dp.message(PrivateFilter(), CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chat_lang = await redis_client.get_user_chat_lang(user_id) or "uz"

    # Fetch user status or initialize if none exists
    user_status = await redis_client.get_user_status(user_id)
    if not user_status:
        user_status = await initialize_user(user_id, chat_lang, state)

    # Handle specific status cases
    if user_status == "CONFIRMATION":
        await handle_confirmation_status(user_id, message, chat_lang, state)
        return

    # Handle subscription and unknown statuses
    if user_status == "COMPLETED":
        await handle_restart_bot(message, chat_lang, state)
        return

    # Process valid statuses
    if user_status in STATUS_HANDLERS:
        await handle_user_status(user_status, message, chat_lang, state)
    else:
        await handle_unknown_status(message, chat_lang, state)


# Helper Functions

async def initialize_user(user_id: int, chat_lang: str, state: FSMContext) -> str:
    """Initialize a user with default status and state."""
    default_status = "DRAFT"
    await redis_client.set_user_status(user_id, default_status)
    await db.add_draft_user(user_id, default_status)
    await state.set_state(RegisterForm.chat_lang)
    await bot.send_message(user_id, await messages.get_message(chat_lang, "welcome"))
    return default_status


async def handle_confirmation_status(user_id: int, message: types.Message, chat_lang: str, state: FSMContext):
    """Handle the CONFIRMATION status."""
    passport = await redis_client.get_user_passport(user_id)
    student = await db.get_student(passport)
    await confirmation(message, chat_lang, student, state)


async def handle_restart_bot(message: types.Message, chat_lang: str, state: FSMContext):
    """Handle cases where the user's status is not recognized."""
    no_subs_channels = await unsubscribed_channels(message.from_user.id)

    if no_subs_channels:
        await message.answer(
            await messages.get_message(chat_lang, "error_subscription"),
            reply_markup=await check_subscribe_keyboard(no_subs_channels, chat_lang),
        )
    else:
        await message.answer(
            await messages.get_message(chat_lang, "restart"),
            reply_markup=await user_menu(chat_lang),
        )
    await state.clear()


async def handle_user_status(user_status: str, message: types.Message, chat_lang: str, state: FSMContext):
    """Handle recognized user statuses dynamically."""
    message_key, keyboard_func, next_state = STATUS_HANDLERS[user_status]

    # Call the keyboard function (supports both sync and async)
    if callable(keyboard_func):
        if asyncio.iscoroutinefunction(keyboard_func):
            keyboard = await keyboard_func(chat_lang)
        else:
            keyboard = keyboard_func(chat_lang)
    else:
        keyboard = keyboard_func

    # Send the message and set the next state
    await message.answer(await messages.get_message(chat_lang, message_key), reply_markup=keyboard)
    if next_state:
        await state.set_state(next_state)

async def handle_unknown_status(message: types.Message, chat_lang: str, state: FSMContext):
    await message.answer(await messages.get_message(chat_lang, "unknown_status"), reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Dynamic Status Handler Mapping
STATUS_HANDLERS = {
    "DRAFT": ("choose_language", choose_language_keyboard, RegisterForm.chat_lang),
    "PHONE_INPUT": ("phone_input", contact_keyboard, RegisterForm.phone),
    "PASSPORT_INPUT": ("passport_input", lambda _: ReplyKeyboardRemove(), RegisterForm.passport),
    "EDIT": ("edit", edit_student_data_keyboard, RegisterForm.edit),
}