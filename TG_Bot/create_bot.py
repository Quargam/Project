from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json
import asyncio

with open("token.json", "r") as token_json:
    token = json.load(token_json)

storage = MemoryStorage()  # Машина состояний (хранение класса в оперативной памяти)
loop = asyncio.get_event_loop()
bot = Bot(token=token["TOKEN"])  # ИНИЦИАЛИЗИРУЕМ БОТА
dp = Dispatcher(bot, storage=storage, loop=loop)  # ИНИЦИАЛИЗИРУЕМ диспетчер
