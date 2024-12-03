from typing import List, Dict
from data.config import PRIVATE_CHANNELS
from utils.misc import get_subscription_status
import asyncio


async def get_or_create_invite_link(chat, user_id: int) -> str:
    from loader import redis_client
    """
    Retrieve or create an invitation link for the user in a specific chat.
    """
    invite_link = await redis_client.get_user_invite_link(user_id)
    if not invite_link:
        invite_link_obj = await chat.create_invite_link(member_limit=1, user_id=user_id)
        invite_link = invite_link_obj.invite_link
        await redis_client.set_user_invite_link(user_id, invite_link)
    return invite_link


async def unsubscribed_channels(user_id: int) -> List[Dict[str, str]]:
    from loader import bot
    """
    Check subscription status of a user in multiple channels and return a list of channels
    where the user is not subscribed or is kicked.
    """
    no_subs_channels = []

    async def check_channel(channel_id):
        try:
            chat = await bot.get_chat(channel_id)
            subs_status = await get_subscription_status(user_id, channel_id)

            if subs_status == "left":
                invite_link = await get_or_create_invite_link(chat, user_id)
                return {"type": "link", "title": chat.title, "link": invite_link}
            elif subs_status == "kicked":
                return {"type": "kicked_message", "title": chat.title}
        except Exception as e:
            # Handle potential errors (e.g., invalid channel_id or permission issues)
            return {"type": "error", "title": str(channel_id)[4:], "message": str(e).replace(": ", " ")[:40]}

    # Run channel checks in parallel
    results = await asyncio.gather(*(check_channel(channel_id) for channel_id in PRIVATE_CHANNELS))
    no_subs_channels.extend(filter(None, results))

    return no_subs_channels


"""
member - obuna bo'lgan foydalanuvchi
administrator - kanal administratori
creator - kanal yaratuvchi

left - chiqib ketgan foydalanuvchi
kicked - kanaldan o'chirilgan foydalanuvchi
restricted - Suhbatda muayyan cheklovlar ostida bo'lgan chat a'zosini ifodalaydi. Faqat superguruhlar.
"""
