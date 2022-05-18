from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data_base import database

class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE

class IsUserAmin(BoundFilter):
    async def check(self, message: types.Message):
        return database.database.admin_exist(message)
class IsNotUserAmin(BoundFilter):
    async def check(self, message: types.Message):
        return not database.database.admin_exist(message)