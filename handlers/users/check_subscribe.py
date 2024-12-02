from aiogram import F
from aiogram.types import CallbackQuery

from data.config import PRIVATE_CHANNELS
from keyboards.default import user_menu
from keyboards.inline import check_subscribe_keyboard
from loader import dp, redis_client, messages, bot
from utils.misc import check_subscription_channel


@dp.callback_query(F.data == 'check_subscribe')
async def check_subscribe(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_lang = await redis_client.get_user_chat_lang(user_id)

    channels_format = await messages.get_message(chat_lang, 'error_subscription')
    no_subs_channels = []

    # Kanallarni tekshirish
    for channel_id in PRIVATE_CHANNELS:
        if not (await check_subscription_channel(callback_query.from_user.id, channel_id)):
            chat = await bot.get_chat(channel_id)
            invite_link_obj = await chat.create_invite_link(member_limit=1)
            no_subs_channels.append({"title": chat.title, "link": invite_link_obj.invite_link})

    # Agar kanalga obuna bo‘lmasa, xabar yuborish va handlerni to‘xtatish
    if no_subs_channels:
        await callback_query.message.edit_text(
            channels_format,
            reply_markup=await check_subscribe_keyboard(no_subs_channels, chat_lang),
            disable_web_page_preview=True
        )
    else:
        await callback_query.message.delete()
        await callback_query.message.answer(
            await messages.get_message(chat_lang, 'success_subscription'),
            reply_markup=await user_menu(chat_lang)
        )
