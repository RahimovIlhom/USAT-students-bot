async def check_subscription_channel(user_id: int, channel_id: int | str) -> bool:
    from loader import bot
    member = await bot.get_chat_member(channel_id, user_id)
    return member.status in ["member", "administrator", "creator"]


async def check_left_subscription_channel(user_id: int, channel_id: int | str) -> bool:
    from loader import bot
    member = await bot.get_chat_member(channel_id, user_id)
    return member.status in ["left", "kicked"]
