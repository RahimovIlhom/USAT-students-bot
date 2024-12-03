from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from keyboards.default import user_menu
from keyboards.inline import check_subscribe_keyboard, CheckSubscribeCallbackData
from loader import dp, redis_client, messages
from utils.misc import unsubscribed_channels


@dp.callback_query(CheckSubscribeCallbackData.filter())
async def check_subscribe(callback_query: CallbackQuery, callback_data: CheckSubscribeCallbackData):
    user_id = callback_query.from_user.id
    chat_lang = await redis_client.get_user_chat_lang(user_id)
    button_type = callback_data.button_type
    data = callback_data.data

    if button_type == 'data' and data == 'check_subscribe':

        no_subs_channels = await unsubscribed_channels(user_id)

        # Agar kanalga obuna bo‘lmasa, xabar yuborish va handlerni to‘xtatish
        if no_subs_channels:
            try:
                await callback_query.message.edit_text(
                    await messages.get_message(chat_lang, 'error_subscription'),
                    reply_markup=await check_subscribe_keyboard(no_subs_channels, chat_lang),
                    disable_web_page_preview=True
                )
            except TelegramBadRequest:
                await callback_query.answer(await messages.get_message(chat_lang, 'error_subscription'), show_alert=True)
        else:
            await callback_query.message.delete()
            await callback_query.message.answer(
                await messages.get_message(chat_lang, 'success_subscription'),
                reply_markup=await user_menu(chat_lang)
            )
            await redis_client.delete_user_invite_link(user_id)
    elif button_type == 'kicked_message':
        await callback_query.answer(await messages.get_message(chat_lang, 'kicked_message'), show_alert=True)
    elif button_type == 'error':
        await callback_query.answer(callback_data.message, show_alert=True)
