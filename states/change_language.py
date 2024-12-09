from aiogram.fsm.state import StatesGroup, State


class ChangeLanguageForm(StatesGroup):
    chat_lang = State()
