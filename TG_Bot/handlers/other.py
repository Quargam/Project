import os.path

from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.utils.markdown import text

# @dp.message_handler()
async def echo_send(message: types.Message):
    pass


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send, content_types=types.message.ContentType.ANY)
