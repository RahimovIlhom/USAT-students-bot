from aiogram.enums import ChatType
from aiogram.types import Message

from filters.channel_filters import ChatTypeFilter
from loader import dp


@dp.message(ChatTypeFilter(chat_type=[ChatType.CHANNEL]))
async def handle_channel_post(message: Message):
    # Kanaldagi xabarni ko'rish
    channel_id = message.chat.id
    text = message.text or message.caption  # Matn yoki caption (agar rasm bo'lsa)

    print(f"Kanal ID: {channel_id}, Post: {text}")

    # Postga javob qaytarish
    await message.answer("Xabar qabul qilindi!")
