from aiogram.filters import BaseFilter

from data.config import ADMINS


class PrivateAdminFilter(BaseFilter):
    async def __call__(self, obj):
        return obj.chat.type == 'private' and str(obj.from_user.id) in ADMINS
