from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

storage = MemoryStorage()  # Машина состояний (хранение класса в оперативной памяти)

# bot = Bot(token=os.getenv('TOKEN'))  # ИНИЦИАЛИЗИРУЕМ БОТА через bat файл
bot = Bot(token="5107816014:AAHjZleLbRnRG-Y1tsKs4XT9yhAO4QmIbek")  # ИНИЦИАЛИЗИРУЕМ БОТА
dp = Dispatcher(bot, storage=storage)  # ИНИЦИАЛИЗИРУЕМ диспетчер
