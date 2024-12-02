from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Update
from loader import dp, bot, redis_client, messages
from data.config import PRIVATE_CHANNELS
from keyboards.inline import check_subscribe_keyboard
from utils.misc import check_subscription_channel
from keyboards.default.user_menu import user_menu_buttons_texts


@dp.update.outer_middleware()
async def check_subs(
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
) -> Any:
    # Faqat xabar bo'lsa, ishlashini ta'minlash
    message = event.message
    if message and message.chat.type == 'private' and message.text in user_menu_buttons_texts['uz'] + \
            user_menu_buttons_texts['ru']:
        user_id = message.from_user.id
        chat_lang = await redis_client.get_user_chat_lang(user_id)

        channels_format = await messages.get_message(chat_lang, 'error_subscription')
        no_subs_channels = []

        # Kanallarni tekshirish
        for channel_id in PRIVATE_CHANNELS:
            if not (await check_subscription_channel(message.from_user.id, channel_id)):
                chat = await bot.get_chat(channel_id)
                invite_link_obj = await chat.create_invite_link(member_limit=1)
                no_subs_channels.append({'link': invite_link_obj.invite_link, 'title': chat.title})

        # Agar kanalga obuna bo‘lmasa, xabar yuborish va handlerni to‘xtatish
        if no_subs_channels:
            await message.answer(
                channels_format,
                reply_markup=await check_subscribe_keyboard(no_subs_channels, chat_lang),
                disable_web_page_preview=True
            )

            return

    # Agar kanalga obuna bo‘lsa, handlerni davom ettiradi
    return await handler(event, data)
