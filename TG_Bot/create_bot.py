from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json
import asyncio

try:
    with open("config_token.json", "r") as token_json:
        token = json.load(token_json)
except FileNotFoundError:
    print(f"exc: FileNotFoundError")
    exit()
bot = Bot(token=token["token"])  # ИНИЦИАЛИЗИРУЕМ БОТА
storage = MemoryStorage()  # Машина состояний (хранение класса в оперативной памяти)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=storage, loop=loop)  # ИНИЦИАЛИЗИРУЕМ диспетчер