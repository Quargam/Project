from aiogram import types, Dispatcher
from create_bot import dp, bot

async def echo_send(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=str(message.chat) + '\n' + str(message.from_user) + '\n' + str(message.sender_chat))



def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send, content_types=types.message.ContentType.ANY)
