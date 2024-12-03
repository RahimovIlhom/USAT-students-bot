import asyncio

from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message

from handlers.users.register import confirmation
from keyboards.inline import get_courses_keyboard, get_edu_directions_keyboard, get_edu_types_keyboard, \
    get_edu_languages_keyboard, CourseNumberCallbackData, EduDirectionCallbackData, EduTypeCallbackData, \
    EduLanguagesCallbackData
from loader import dp, redis_client, messages, db
from states import RegisterForm


@dp.callback_query(StateFilter(RegisterForm.edit, State()), F.data == 'edit_fullname')
async def edit_fullname(callback_query: CallbackQuery, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    await callback_query.message.edit_text(await messages.get_message(chat_lang, "edit_fullname"),
                                           reply_markup=None)
    await state.set_state(RegisterForm.edit_fullname)


@dp.message(RegisterForm.edit_fullname, lambda msg: msg.content_type == ContentType.TEXT)
async def send_fullname(message: Message, state: FSMContext):
    user_id = message.from_user.id
    fullname = message.text.strip()
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    passport = await redis_client.get_user_passport(message.from_user.id)

    await db.set_student_fullname(passport, fullname)

    # Check if student exists in the database
    student = await db.get_student(passport)

    await confirmation(message, chat_lang, student, state)

    # Update database and Redis with new user state
    await db.update_user_status(user_id, 'CONFIRMATION')
    await redis_client.set_user_status(user_id, 'CONFIRMATION')

    await state.set_state(RegisterForm.confirm)


@dp.callback_query(StateFilter(RegisterForm.edit, State()), F.data == 'edit_course')
async def edit_course(callback_query: CallbackQuery, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    await callback_query.message.edit_text(await messages.get_message(chat_lang, "edit_course"),
                                           reply_markup=await get_courses_keyboard(chat_lang))
    await state.set_state(RegisterForm.edit_course)


@dp.callback_query(StateFilter(RegisterForm.edit_course, State()), CourseNumberCallbackData.filter())
async def input_course(callback_query: CallbackQuery, callback_data: CourseNumberCallbackData, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    course_num = callback_data.course_number
    passport = await redis_client.get_user_passport(callback_query.from_user.id)

    await db.set_student_course(passport, course_num)

    # Check if student exists in the database
    student = await db.get_student(passport)

    await confirmation(callback_query, chat_lang, student, state)

    # Update database and Redis with new user state
    await db.update_user_status(callback_query.from_user.id, 'CONFIRMATION')
    await redis_client.set_user_status(callback_query.from_user.id, 'CONFIRMATION')

    await state.set_state(RegisterForm.confirm)


@dp.callback_query(StateFilter(RegisterForm.edit, State()), F.data == 'edit_edu_direction')
async def edit_edu_direction(callback_query: CallbackQuery, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    await callback_query.message.edit_text(await messages.get_message(chat_lang, "edit_edu_direction"),
                                           reply_markup=await get_edu_directions_keyboard(chat_lang))
    await state.set_state(RegisterForm.edit_edu_direction)


@dp.callback_query(StateFilter(RegisterForm.edit_edu_direction, State()), EduDirectionCallbackData.filter())
async def input_edu_direction(callback_query: CallbackQuery, callback_data: EduDirectionCallbackData, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    edu_direction_id = int(callback_data.edu_direction_id)
    passport = await redis_client.get_user_passport(callback_query.from_user.id)

    await db.set_student_edu_direction(passport, edu_direction_id)

    # Check if student exists in the database
    student = await db.get_student(passport)

    await confirmation(callback_query, chat_lang, student, state)

    # Update database and Redis with new user state
    await db.update_user_status(callback_query.from_user.id, 'CONFIRMATION')
    await redis_client.set_user_status(callback_query.from_user.id, 'CONFIRMATION')

    await state.set_state(RegisterForm.confirm)


@dp.callback_query(StateFilter(RegisterForm.edit, State()), F.data == 'edit_edu_type')
async def edit_edu_type(callback_query: CallbackQuery, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    await callback_query.message.edit_text(await messages.get_message(chat_lang, "edit_edu_type"),
                         reply_markup=await get_edu_types_keyboard(chat_lang))
    await state.set_state(RegisterForm.edit_edu_type)


@dp.callback_query(StateFilter(RegisterForm.edit_edu_type, State()), EduTypeCallbackData.filter())
async def input_edu_type(callback_query: CallbackQuery, callback_data: EduTypeCallbackData, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    edu_type_id = int(callback_data.edu_type_id)
    passport = await redis_client.get_user_passport(callback_query.from_user.id)

    await db.set_student_edu_type(passport, edu_type_id)

    # Check if student exists in the database
    student = await db.get_student(passport)

    await confirmation(callback_query, chat_lang, student, state)

    # Update database and Redis with new user state
    await db.update_user_status(callback_query.from_user.id, 'CONFIRMATION')
    await redis_client.set_user_status(callback_query.from_user.id, 'CONFIRMATION')

    await state.set_state(RegisterForm.confirm)


@dp.callback_query(StateFilter(RegisterForm.edit, State()), F.data == 'edit_edu_lang')
async def edit_edu_lang(callback_query: CallbackQuery, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    await callback_query.message.edit_text(await messages.get_message(chat_lang, "edit_edu_lang"),
                         reply_markup=await get_edu_languages_keyboard(chat_lang))
    await state.set_state(RegisterForm.edit_edu_lang)


@dp.callback_query(StateFilter(RegisterForm.edit_edu_lang, State()), EduLanguagesCallbackData.filter())
async def input_edu_lang(callback_query: CallbackQuery, callback_data: EduLanguagesCallbackData, state: FSMContext):
    chat_lang = await redis_client.get_user_chat_lang(callback_query.from_user.id)
    edu_lang = callback_data.lang
    passport = await redis_client.get_user_passport(callback_query.from_user.id)

    await db.set_student_edu_lang(passport, edu_lang)

    # Check if student exists in the database
    student = await db.get_student(passport)

    await confirmation(callback_query, chat_lang, student, state)

    # Update database and Redis with new user state
    await db.update_user_status(callback_query.from_user.id, 'CONFIRMATION')
    await redis_client.set_user_status(callback_query.from_user.id, 'CONFIRMATION')

    await state.set_state(RegisterForm.confirm)


@dp.message(StateFilter(RegisterForm))
async def err_message(message: Message):
    await message.delete()

    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    warning_msg = await message.answer(await messages.get_message(chat_lang, 'warning_msg'))
    await asyncio.sleep(5)
    await warning_msg.delete()
