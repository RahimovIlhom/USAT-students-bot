from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message

from filters.private_filters import PrivateFilter
from keyboards.default import user_menu_buttons_texts, settings_keyboard, settings_buttons_texts, \
    choose_language_keyboard
from loader import dp, messages, redis_client, db
from states import ChangeLanguageForm


@dp.message(PrivateFilter(), State(), F.text.in_(user_menu_buttons_texts['uz'][1] + user_menu_buttons_texts['ru'][1]))
async def settings(message: Message):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await message.answer(await messages.get_message('uz', 'settings'), reply_markup=await settings_keyboard(chat_lang))


@dp.message(PrivateFilter(), State(), F.text.in_(settings_buttons_texts['uz'][0] + settings_buttons_texts['ru'][0]))
async def settings(message: Message, state: FSMContext):
    await message.answer(await messages.get_message('uz', 'settings_language'), reply_markup=choose_language_keyboard)
    await state.set_state(ChangeLanguageForm.chat_lang)


CHAT_LANGUAGES = {
    '🇺🇿 O‘zbek tili': 'uz',
    '🇷🇺 Русский язык': 'ru'
}

@dp.message(ChangeLanguageForm.chat_lang, F.text.in_(['🇺🇿 O‘zbek tili', '🇷🇺 Русский язык']))
async def set_language(message: Message, state: FSMContext):
    lang = CHAT_LANGUAGES[message.text]
    await message.answer(await messages.get_message(lang, 'settings_language_changed'), reply_markup=await settings_keyboard(lang))
    await redis_client.set_user_chat_lang(message.from_user.id, lang)
    await db.set_chat_lang(message.from_user.id, lang)
    await state.clear()
