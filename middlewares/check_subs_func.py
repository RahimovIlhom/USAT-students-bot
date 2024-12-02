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
        final_status = True

        # Kanallarni tekshirish
        for channel_id in PRIVATE_CHANNELS:
            chat = await bot.get_chat(channel_id)
            invite_link = await chat.export_invite_link()
            status = not (await check_subscription_channel(message.from_user.id, channel_id))
            final_status *= status
            if status:
                channels_format += f"\n<a href='{invite_link}'>{chat.title}</a>"

        # Agar kanalga obuna bo‘lmasa, xabar yuborish va handlerni to‘xtatish
        if final_status:
            await message.answer(
                channels_format,
                reply_markup=await check_subscribe_keyboard(chat_lang),
                disable_web_page_preview=True
            )

            return

    # Agar kanalga obuna bo‘lsa, handlerni davom ettiradi
    return await handler(event, data)
