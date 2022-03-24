from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='5107816014:AAHjZleLbRnRG-Y1tsKs4XT9yhAO4QmIbek')  # ИНИЦИАЛИЗИРУЕМ БОТА
dp = Dispatcher(bot, storage=storage)  # ИНИЦИАЛИЗИРУЕМ диспетчер
