from aiogram import types, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import contact_keyboard
from keyboards.inline import registration_confirmation_keyboard
from loader import dp, redis_client, messages, db
from states import RegisterForm


async def set_language_and_proceed(user_id, lang, state: FSMContext):
    """Foydalanuvchi tilini o'rnatish va keyingi bosqichga o'tish."""
    await redis_client.set_user_status(user_id, 'PHONE_INPUT')
    await redis_client.set_user_chat_lang(user_id, lang)
    await db.update_user_language(user_id, lang, 'PHONE_INPUT')
    await state.set_state(RegisterForm.phone)
    return await contact_keyboard(lang)


@dp.message(RegisterForm.chat_lang, F.text.in_(['🇺🇿 O\'zbek tili', '🇷🇺 Русский язык']))
async def set_language(message: types.Message, state: FSMContext):
    lang = 'uz' if message.text == '🇺🇿 O\'zbek tili' else 'ru'
    chat_keyboard = await set_language_and_proceed(message.from_user.id, lang, state)
    await message.answer(await messages.get_message(lang, 'phone_input'), reply_markup=chat_keyboard)


@dp.message(RegisterForm.chat_lang, lambda msg: msg.content_type == ContentType.ANY)
async def err_choose_language(message: types.Message):
    await message.delete()
    await message.answer(await messages.get_message('uz', 'choose_language'))


@dp.message(RegisterForm.phone, F.content_type == ContentType.CONTACT)
async def set_phone(message: types.Message, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await db.update_user_phone(message.from_user.id, message.contact.phone_number, 'PASSPORT_INPUT')
    await redis_client.set_user_status(message.from_user.id, 'PASSPORT_INPUT')
    await state.set_state(RegisterForm.passport)
    await message.answer(await messages.get_message(chat_lang, 'passport_input'), reply_markup=ReplyKeyboardRemove())


@dp.message(RegisterForm.phone, F.content_type == ContentType.ANY)
async def err_phone(message: types.Message):
    await message.delete()
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await message.answer(await messages.get_message(chat_lang, 'phone_input'),
                         reply_markup=await contact_keyboard(chat_lang))

# Regex pattern: AA1234567
PASSPORT_REGEX = r'^[A-Z]{2}\d{7}$'


@dp.message(RegisterForm.passport, F.text.regexp(PASSPORT_REGEX))
async def set_passport(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chat_lang = await redis_client.get_user_chat_lang(user_id)
    passport = message.text.upper()

    # Check if student exists in the database
    student = await db.get_student(passport)
    if not student:
        await message.answer(await messages.get_message(chat_lang, 'passport_not_found'))
        return

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
    await message.answer(answer_text, reply_markup=await registration_confirmation_keyboard(chat_lang))

    # Update database and Redis with new user state
    await db.update_user_passport(user_id, student['id'], 'CONFIRMATION')
    await redis_client.set_user_status(user_id, 'CONFIRMATION')
    await state.set_state(RegisterForm.confirm)


@dp.message(RegisterForm.passport, lambda msg: msg.content_type == ContentType.TEXT)
async def invalid_passport(message: types.Message):
    await message.delete()
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await message.answer(await messages.get_message(chat_lang, 'invalid_passport'))
