async def get_subscription_status(user_id: int, channel_id: int | str) -> bool:
    from loader import bot
    return (await bot.get_chat_member(channel_id, user_id)).status
