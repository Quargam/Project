from aiogram.utils import executor
from create_bot import dp, bot
from data_base import sqlite_db

async def on_startup(_):
    print('Бот стал онлайн')
    # await bot.send_message(1116537818, 'Бот стал онлайн')
    sqlite_db.sql_start()


from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_client(dp)
other.register_handlers_other(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # запуск бота

