from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other # Импортируем клиенскую, админскую и остальную часть кода
from data_base import database
import Filter

async def on_startup(_): # Сбытие которое должно выполнится 1 раз при запуске
    database.first_set_config()
    try:
        """
        Так как я не знаю как отслеживать изменения статуса админов, то просто каждый раз и обновляю их список
        !нужно узнать как это сделать на 2.* версии aiogram!
        """
        database.database.admin_del_all()
        await database.database.add_admins()
    except:
        pass
    Filter.setup(dp)

admin.register_handlers_admins(dp)  # админские функции
client.register_handlers_client(dp)  # клиенские функции
other.register_handlers_other(dp)  # остальные функции


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # запуск бота
    except Exception as exc:
        print(exc)

