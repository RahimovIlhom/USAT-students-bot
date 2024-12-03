from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Update, ReplyKeyboardRemove

from loader import dp, redis_client, messages


async def send_blocked_message(event, chat_lang):
    """Bloklangan foydalanuvchiga xabar yuborish."""
    blocked_message = await messages.get_message(chat_lang, "blocked")

    if event.message:
        # Handle message type
        await event.message.answer(blocked_message, reply_markup=ReplyKeyboardRemove())
    elif event.callback_query:
        # Handle callback_query type
        await event.callback_query.message.edit_text(blocked_message, reply_markup=None)


@dp.update.outer_middleware()
async def check_blocked_user_middleware(
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
) -> Any:
    """Bloklangan foydalanuvchilarning so'rovlarini qaytarish."""
    user_id = event.message.from_user.id if event.message else event.callback_query.from_user.id
    chat_lang = await redis_client.get_user_chat_lang(user_id)
    user_status = await redis_client.get_user_status(user_id)

    # Bloklangan foydalanuvchini tekshirish
    if user_status == "BLOCKED":
        await send_blocked_message(event, chat_lang)
        return  # Bloklangan foydalanuvchining so'rovini rad etish

    return await handler(event, data)
