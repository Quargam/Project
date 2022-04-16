import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

loop = asyncio.get_event_loop()
bot = Bot(token='5107816014:AAHjZleLbRnRG-Y1tsKs4XT9yhAO4QmIbek')  # ИНИЦИАЛИЗИРУЕМ БОТА
dp = Dispatcher(bot, loop=loop)  # ИНИЦИАЛИЗИРУЕМ диспетчер

scheduler = AsyncIOScheduler()
TimerFlag = False

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('привет')
    print(datetime.datetime.now())

async def send_channel():
    await bot.send_message(chat_id=-1001529216403, text= str(datetime.datetime.now()))

def timer():
    global scheduler
    scheduler.add_job(send_channel, 'interval', seconds=60)
    scheduler.start()

@dp.message_handler(commands=['timer'])
async def start(message: types.Message):
    global TimerFlag
    if TimerFlag is False:
        await message.answer('timer start')
        timer()
        TimerFlag = True
    else:
        await message.answer('timer is running')

@dp.message_handler(commands=['timeroff'])
async def start(message: types.Message):
    global TimerFlag, scheduler
    if TimerFlag is False:
        pass
    else:
        scheduler.shutdown()
        TimerFlag = False

if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)  # запуск бота
