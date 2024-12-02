from aiogram.filters import BaseFilter


class ChannelPostFilter(BaseFilter):
    async def __call__(self, obj):
        return obj.chat.type == 'channel'
