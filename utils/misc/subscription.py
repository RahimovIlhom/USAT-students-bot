async def check_subscription(user_id: int, channel_id: int | str) -> bool:
    from loader import bot
    member = await bot.get_chat_member(channel_id, user_id)
    return member.is_member
