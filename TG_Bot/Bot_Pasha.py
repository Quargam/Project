from aiogram.utils import executor
from create_bot import dp, bot
from data_base import sqlite_db
# import asyncio


# Сбытие которое должно выполнится 1 раз при запуске
async def on_startup(_):
    print('Бот стал онлайн')
    await bot.send_message(1116537818, 'Бот стал онлайн')
    print(bot.__dict__)
    sqlite_db.sql_start() # подключение к БД

# Импортируем клиенскую, админскую и остальную часть кода
from handlers import client, admin, other

client.register_handlers_client(dp) # клиенские функции
admin.register_handlers_client(dp) # админские функции
other.register_handlers_other(dp) # остальные функции


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # запуск бота

