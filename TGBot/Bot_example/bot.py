import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
import schedule
import asyncio
import time
import datetime

loop = asyncio.get_event_loop()
bot = Bot(token='5107816014:AAHjZleLbRnRG-Y1tsKs4XT9yhAO4QmIbek')  # ИНИЦИАЛИЗИРУЕМ БОТА
dp = Dispatcher(bot, loop=loop)  # ИНИЦИАЛИЗИРУЕМ диспетчер


# @dp.message_handler()
# async def time():
#     while True:
#         await asyncio.sleep(10)
#         await bot.send_message(chat_id= -1001529216403,text='отправка сообщения')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('привет')
    print(datetime.datetime.now())


# await bot.send_message(chat_id=-1001529216403, text='отправка сообщения каждый час')
# await asyncio.sleep(60 * 60)
# print(datetime.datetime.now())
async def counter():
    one_Lessons = True
    two_Lessons = True
    three_Lessons = True
    four_Lessons = True
    five_Lessons = True
    six_Lessons = True
    seven_Lessons = True
    eight_Lessons = True
    while True:
        # print(str(datetime.datetime.now()).split(' ')[1][:5])
        await asyncio.sleep(55)
        if str(datetime.datetime.now()).split(' ')[1][:5] >= '09:00' and str(datetime.datetime.now()).split(' ')[1][
                                                                         :5] <= '10:45' and one_Lessons:
            await bot.send_message(chat_id=-1001529216403, text='09.00')
            one_Lessons = False
            seven_Lessons = True
        if str(datetime.datetime.now()).split(' ')[1][:5] >= '10:45' and str(datetime.datetime.now()).split(' ')[1][
                                                                         :5] <= '12:20' and two_Lessons:
            await bot.send_message(chat_id=-1001529216403, text='10.45')
            two_Lessons = False
        if str(datetime.datetime.now()).split(' ')[1][:5] >= '12:20' and str(datetime.datetime.now()).split(' ')[1][
                                                                         :5] <= '13:55' and three_Lessons:
            # print(str(datetime.datetime.now()).split(' ')[1][:5])
            # print(three_Lessons)
            await bot.send_message(chat_id=-1001529216403, text='12.20')
            three_Lessons = False
        if str(datetime.datetime.now()).split(' ')[1][:5] >= '13:55' and str(datetime.datetime.now()).split(' ')[1][
                                                                         :5] <= '15:30' and four_Lessons:
            await bot.send_message(chat_id=-1001529216403, text='13.55')
            four_Lessons = False
        if str(datetime.datetime.now()).split(' ')[1][:5] >= '15:30' and str(datetime.datetime.now()).split(' ')[1][
                                                                         :5] <= '17:05' and five_Lessons:
            await bot.send_message(chat_id=-1001529216403, text='15.30')
            five_Lessons = False
        if str(datetime.datetime.now()).split(' ')[1][:5] >= '17:05' and str(datetime.datetime.now()).split(' ')[1][
                                                                         :5] <= '20:00' and six_Lessons:
            await bot.send_message(chat_id=-1001529216403, text='17.05')
            six_Lessons = False
        if str(datetime.datetime.now()).split(' ')[1][:5] >= '20:00' and seven_Lessons:
            await bot.send_message(chat_id=-1001529216403, text='обнуление значений')
            one_Lessons = True
            two_Lessons = True
            three_Lessons = True
            four_Lessons = True
            five_Lessons = True
            six_Lessons = True
            seven_Lessons = False
            # eight_Lessons = True
            print("asdsfdsffdfd")


if __name__ == '__main__':
    loop.create_task(counter())
    executor.start_polling(dp, loop=loop, skip_updates=True)  # запуск бота
