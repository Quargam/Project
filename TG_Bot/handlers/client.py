from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db, db

db_users = db.Database_users("Users_db.db")

# Действия когда пользователь вводит команду /start
async def command_start(message: types.Message):
    if message.chat.type == 'private':
        if not db_users.user_exists(message.from_user.id, 'users'):
            db_users.add_user(message.from_user.id, 'users')
            await bot.send_message(message.from_user.id, 'добавлен в базу данных', reply_markup=kb_client)
        await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=kb_client)
    else:
        await message.reply('общение с ботом через ЛС, напишите ему:\n https://t.me/HyperPashaBot')
    await message.delete()

# @dp.message_handler(commands=['Мероприятие'])
async def event_menu_command(message: types.Message):
    # for ret in cur.execute('SELECT * FROM menu').fetchall():
    #     await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
    await sqlite_db.sql_read(message)
    await message.delete()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(event_menu_command, commands=['Мероприятие'])