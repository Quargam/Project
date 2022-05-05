from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db, db
import ast
import json

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
    # await message.delete()

# @dp.message_handler(commands=['места_занятий'])
async def place_menu_command(message: types.Message):
    await sqlite_db.sql_read_place(message)
    # await message.delete()

# Выводит расписание преподавателей
async def schedule(message: types.Message):
    try:
        with open("schedule.json", "r", encoding='utf-8') as schedule_json:
            schedule = json.load(schedule_json)
        await bot.send_message(message.from_user.id,
                               text='\n'.join(list(f'{Days[day]} - {schedule[str(day)]}' for day in range(6)))
                                    + '\nв 17.05 только по расписанию')
    except FileNotFoundError:
        await bot.send_message(message.from_user.id, text='файл не найден')

# # Выводит Нормативы
async def exercise_standards(message: types.Message):
    try:
        with open("exercise_standards.json", "r", encoding='utf-8') as exercise_standards_json:
            exercise_standards = json.load(exercise_standards_json)
        await bot.send_photo(message.from_user.id, exercise_standards["photo_exercise_standards"],
                             f'Описание:{exercise_standards["text_exercise_standards"]}\n')
    except FileNotFoundError:
        await bot.send_message(message.from_user.id, text='файл не найден')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(event_menu_command, text='🆕 новости')
    dp.register_message_handler(schedule, text='📝 расписание')
    dp.register_message_handler(exercise_standards, text='🏃 нормативы')
    dp.register_message_handler(place_menu_command, text='🚩 места занятий')