from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db, db
import ast

db_users = db.Database_users("Users_db.db")
Days = {0: "пн", 1: "вт", 2: "ср", 3: "чт", 4: "пт", 5: "сб", 6: "вс"}

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

async def event_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)
    await message.delete()

@dp.message_handler(commands=['места_занятий'])
async def place_menu_command(message: types.Message):
    await sqlite_db.sql_read_place(message)
    await message.delete()

# Выводит расписание преподавателей
async def schedule(message: types.Message):
    try:
        file = open("schedule.txt", encoding='utf-8')
        res_dict = ast.literal_eval(file.read())
        await bot.send_message(message.from_user.id, text ='\n'.join(list(f'{Days[day]} - {res_dict[str(day)]}' for day in range(6))))
    except FileNotFoundError:
        await bot.send_message(message.from_user.id, text='файл не найден')

# # Выводит Нормативы
@dp.message_handler(commands=['Нормативы'])
async def exercise_standards(message: types.Message):
    try:
        file = open("exercise_standards.txt")
        res_dict = ast.literal_eval(file.read())
        await bot.send_photo(message.from_user.id, res_dict[0], f'Описание:{res_dict[1]}\n')
    except FileNotFoundError:
        await bot.send_message(message.from_user.id, text='файл не найден')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(event_menu_command, commands=['Мероприятие'])
    dp.register_message_handler(schedule, commands=['Расписание'])