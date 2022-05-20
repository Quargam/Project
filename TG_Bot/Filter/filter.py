from aiogram import types
from aiogram.types import ChatMemberUpdated
from aiogram.dispatcher.filters import BoundFilter
from data_base import database


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsUserAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return database.database.admin_exist(message)


class IsNotUserAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return not database.database.admin_exist(message)