from aiogram import types, Dispatcher

async def echo_send(message: types.Message):
    pass

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send, content_types=types.message.ContentType.ANY)
