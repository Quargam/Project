from aiogram import types, Dispatcher
from create_bot import dp, bot



# @dp.message_handler()
async def echo_send(message: types.Message):
    if message.text.lower() == 'ок' or 'ok':
        await message.answer("пидарок")
    else:
        await message.answer(message.text)  # отправляет полученное текствое сообщение


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
