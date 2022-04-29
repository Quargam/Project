import os.path

from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.utils.markdown import text


async def download_file(message: types.Message):
    file_id = message.photo[2].file_id
    file_info = await bot.get_file(file_id)
    print(file_info)
    print(file_id)
    # await bot.download_file_by_id(file_id, destination=r'C:\Users\Lenovo\Desktop\python\TGBot\HPB\' + f'{file_id}.jpg')
    print(os.getcwd())
    # path = file_id + ".jpg"
    # file_info = bot.get_file(file_id)
    # downloaded_file = bot.download_file(file_info.file_path)
    # with open(path, 'wb') as new_file:
    #     new_file.write(downloaded_file)
    # await bot.send_photo(chat_id=-1001529216403, photo=file_id)


# @dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(text(message.content_type, message.message_id, message.from_user, message.date, message.chat,
                              message.forward_from_chat, message.caption, message.photo, message.forward_from,
                              message.reply_to_message, 'пидорас паша', sep='\n'))
    # print(message.photo[0]["file_id"])
    # await bot.send_message(chat_id= -1001529216403,text='отправка сообщения')


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(download_file, content_types=types.message.ContentType.PHOTO)
    dp.register_message_handler(echo_send, content_types=types.message.ContentType.ANY)
