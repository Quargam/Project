from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.utils.markdown import text

# @dp.message_handler()
async def echo_send(message: types.Message):
    print(message.location)
#     await bot.send_message(message.from_user.id, text='место:Бассейн\nместо сбора учащихся\n⬇⬇⬇')
#     await bot.send_venue(message.from_user.id, 55.928782, 37.524395, title='Бассейн',
#                          address='Московское ш., 21, корп. 1')


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send, content_types=types.message.ContentType.ANY)
