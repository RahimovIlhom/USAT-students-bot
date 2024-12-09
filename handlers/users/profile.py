from aiogram import F
from aiogram.types import Message

from filters.private_filters import PrivateFilter
from handlers.users.download_ticket import handle_ticket_image
from keyboards.default import user_menu_buttons_texts, profile_menu, profile_buttons_texts
from loader import dp, redis_client, messages, db


@dp.message(PrivateFilter(), F.text.in_(user_menu_buttons_texts['uz'][2] + user_menu_buttons_texts['ru'][2]))
async def profile(message: Message):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    await message.answer(await messages.get_message(chat_lang, 'profile'), reply_markup=await profile_menu(chat_lang))


@dp.message(PrivateFilter(), F.text.in_(profile_buttons_texts['uz'][0] + profile_buttons_texts['ru'][0]))
async def get_my_profile(message: Message):
    # Foydalanuvchining chat tilini aniqlash
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    tg_id = message.from_user.id

    # Foydalanuvchi ma'lumotlarini olish
    user_data = await db.get_user(tg_id)

    # Agar foydalanuvchi ma'lumotlari topilmasa
    if not user_data:
        error_message = {
            "uz": "❌ Maʼlumotlar topilmadi.",
            "ru": "❌ Данные не найдены."
        }.get(chat_lang, "❌ Maʼlumotlar topilmadi.")  # Default holat
        await message.answer(error_message, parse_mode="HTML")
        return

    # Profil uchun kerakli til va qiymatlarni aniqlash
    profile_text = {
        "uz": f"""
<b>Sizning profilingiz:</b>\n\n
<i>FIO:</i> {user_data['student_fullname']}\n
<i>Passport:</i> {user_data['student_passport']}\n
<i>Kurs:</i> {user_data['student_course']}\n
<i>Til:</i> {user_data['student_edu_lang']}\n
<i>Ta’lim yo‘nalishi:</i> {user_data['edu_direction_name_uz']}\n
<i>Ta’lim turi:</i> {user_data['edu_type_name_uz']}\n
<i>Telefon:</i> {user_data['phone']}\n
<i>Ro‘yxatdan o‘tgan sana:</i> {user_data['created_at'].strftime('%Y-%m-%d %H:%M:%S')}
""",
        "ru": f"""
<b>Ваш профиль:</b>\n\n
<i>ФИО:</i> {user_data['student_fullname']}\n
<i>Паспорт:</i> {user_data['student_passport']}\n
<i>Курс:</i> {user_data['student_course']}\n
<i>Язык:</i> {user_data['student_edu_lang']}\n
<i>Направление обучения:</i> {user_data['edu_direction_name_ru']}\n
<i>Тип обучения:</i> {user_data['edu_type_name_ru']}\n
<i>Телефон:</i> {user_data['phone']}\n
<i>Дата регистрации:</i> {user_data['created_at'].strftime('%Y-%m-%d %H:%M:%S')}
"""
    }.get(chat_lang, "")

    # Profil ma'lumotlarini yuborish
    await message.answer(profile_text, parse_mode="HTML")


@dp.message(PrivateFilter(), F.text.in_(profile_buttons_texts['uz'][1] + profile_buttons_texts['ru'][1]))
async def get_my_ticket(message: Message):
    chat_lang = await redis_client.get_user_chat_lang(message.from_user.id)
    image = await db.get_my_ticket_image(message.from_user.id)

    if image:
        image_url = await handle_ticket_image(image)
        try:
            await message.answer_photo(image_url, caption=await messages.get_message(chat_lang, 'ticket'))
        except Exception as e:
            await message.answer(str(e))
    else:
        await message.answer(await messages.get_message(chat_lang, 'no_ticket'))
