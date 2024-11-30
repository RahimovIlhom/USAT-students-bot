from aiogram.fsm.state import StatesGroup, State


class RegisterForm(StatesGroup):
    chat_lang = State()
    phone = State()
    passport = State()
    confirm = State()
    edit = State()
    edit_fullname = State()
    edit_course = State()
    edit_edu_direction = State()
    edit_edu_type = State()
    edit_edu_lang = State()
