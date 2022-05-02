from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


storage = MemoryStorage()  # Машина состояний (хранение класса в оперативной памяти)
loop = asyncio.get_event_loop()

# bot = Bot(token=os.getenv('TOKEN'))  # ИНИЦИАЛИЗИРУЕМ БОТА через bat файл
bot = Bot(token=open('token.txt').read())  # ИНИЦИАЛИЗИРУЕМ БОТА
dp = Dispatcher(bot, storage=storage, loop=loop)  # ИНИЦИАЛИЗИРУЕМ диспетчер
