from aiogram import F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, Message

from data.config import PRIVATE_CHANNELS
from keyboards.default import contact_keyboard, user_menu
from keyboards.inline import registration_confirmation_keyboard, edit_student_data_keyboard, check_subscribe_keyboard
from loader import dp, redis_client, messages, db, bot
from states import RegisterForm
from utils.misc import check_subscription_channel


async def set_language_and_proceed(user_id, lang, state: FSMContext):
    """Foydalanuvchi tilini o'rnatish va keyingi bosqichga o'tish."""
    await redis_client.set_user_status(user_id, 'PHONE_INPUT')
    await redis_client.set_user_chat_lang(user_id, lang)
    await db.update_user_language(user_id, lang, 'PHONE_INPUT')
    await state.set_state(RegisterForm.phone)
    return await contact_keyboard(lang)


@dp.message(RegisterForm.chat_lang, F.text.in_(['🇺🇿 O\'zbek tili', '🇷🇺 Русский язык']))
async def set_language(message: Message, state: FSMContext):
    lang = 'uz' if message.text == '🇺🇿 O\'zbek tili' else 'ru'
    chat_keyboard = await set_language_and_proceed(message.from_user.id, lang, state)
    await message.answer(await messages.get_message(lang, 'phone_input'), reply_markup=chat_keyboard)


@dp.message(RegisterForm.chat_lang, lambda msg: msg.content_type == ContentType.TEXT)
async def err_choose_language(message: Message):
    await message.delete()
    await message.answer(await messages.get_message('uz', 'choose_language'))


@dp.message(RegisterForm.phone, F.content_type == ContentType.CONTACT)
async def set_phone(message: Message, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await db.update_user_phone(message.from_user.id, message.contact.phone_number, 'PASSPORT_INPUT')
    await redis_client.set_user_status(message.from_user.id, 'PASSPORT_INPUT')
    await state.set_state(RegisterForm.passport)
    await message.answer(await messages.get_message(chat_lang, 'passport_input'), reply_markup=ReplyKeyboardRemove())


@dp.message(RegisterForm.phone, F.content_type == ContentType.TEXT)
async def err_phone(message: Message):
    await message.delete()
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await message.answer(await messages.get_message(chat_lang, 'phone_input'),
                         reply_markup=await contact_keyboard(chat_lang))

# Regex pattern: AA1234567
PASSPORT_REGEX = r'^[a-zA-Z]{2}\d{7}$'


async def confirmation(update: Message | CallbackQuery, chat_lang, student, state):
    # Prepare confirmation message with student information
    student_info = await messages.get_message(chat_lang, 'student_info')
    register_confirmation = await messages.get_message(chat_lang, 'register_confirmation')
    language_name = "O'zbek" if chat_lang == 'uz' else 'Русский'

    answer_text = (
            f"{register_confirmation}\n\n" +
            student_info.format(
                F=student['fullname'],
                N=student['course'],
                X=student[f'edu_direction_name_{chat_lang}'],
                Y=student[f'edu_type_name_{chat_lang}'],
                U=language_name
            )
    )
    if isinstance(update, CallbackQuery):
        await update.message.edit_text(answer_text, reply_markup=await registration_confirmation_keyboard(chat_lang))
    else:
        await update.answer(answer_text, reply_markup=await registration_confirmation_keyboard(chat_lang))
    await state.set_state(RegisterForm.confirm)


@dp.message(RegisterForm.passport, F.text.regexp(PASSPORT_REGEX))
async def set_passport(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_lang = await redis_client.get_user_chat_lang(user_id)
    passport = message.text.upper()

    # Check if student exists in the database
    student = await db.get_student(passport)
    if not student:
        await message.answer(await messages.get_message(chat_lang, 'passport_not_found'))
        return

    await confirmation(message, chat_lang, student, state)

    # Update database and Redis with new user state
    await db.update_user_passport(user_id, student['id'], 'CONFIRMATION')
    await redis_client.set_user_status(user_id, 'CONFIRMATION')
    await redis_client.set_user_passport(user_id, passport)


@dp.message(RegisterForm.passport, lambda msg: msg.content_type == ContentType.TEXT)
async def invalid_passport(message: Message):
    await message.delete()
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await message.answer(await messages.get_message(chat_lang, 'invalid_passport'))


@dp.callback_query(RegisterForm.confirm, F.data == 'registration_confirmation_edit')
async def edit_student_data(callback_query: CallbackQuery, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    await callback_query.message.edit_text(await messages.get_message(chat_lang, 'edit'),
                                           reply_markup=await edit_student_data_keyboard(chat_lang))
    await redis_client.set_user_status(callback_query.from_user.id, 'EDIT')
    await db.update_user_status(callback_query.from_user.id, 'EDIT')
    await state.set_state(RegisterForm.edit)


@dp.callback_query(RegisterForm.confirm, F.data == 'registration_confirm')
async def confirm_registration(callback_query: CallbackQuery, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    channels_format = await messages.get_message(chat_lang, 'register_completed')
    no_subs_channels = []

    for channel_id in PRIVATE_CHANNELS:
        if not (await check_subscription_channel(callback_query.from_user.id, channel_id)):
            chat = await bot.get_chat(channel_id)
            invite_link_obj = await chat.create_invite_link(member_limit=1)
            no_subs_channels.append({'title': chat.title, 'link': invite_link_obj.invite_link})

    if no_subs_channels:
        await callback_query.message.edit_text(channels_format,
                                               reply_markup=await check_subscribe_keyboard(no_subs_channels, chat_lang))
    else:
        await callback_query.message.delete()
        await callback_query.message.answer(await messages.get_message(chat_lang, 'register_completed2'),
                                               reply_markup=await user_menu(chat_lang))
    await redis_client.set_user_status(callback_query.from_user.id, 'COMPLETED')
    await db.update_user_status(callback_query.from_user.id, 'COMPLETED')
    await state.clear()
