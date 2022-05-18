from cgitb import text
import datetime
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import database
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Text
import asyncio
from Filter import IsPrivate, IsUserAmin, IsNotUserAmin

Days = {0: "пн", 1: "вт", 2: "ср", 3: "чт", 4: "пт", 5: "сб", 6: "вс"}


# Действия когда пользователь вводит команду /start
async def command_start(message: types.Message):
    if message.chat.type == 'private':
        if not database.database.student_exist(message):
            database.database.student_add(message)
        await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=kb_client)
    else:
        await message.reply('общение с ботом через ЛС, напишите ему:\n https://t.me/HyperPashaBot')
    await message.delete()


async def news_menu(message: types.Message):
    news_data = database.database.news_read()
    for new in news_data:
        await bot.send_photo(message.from_user.id, new[1], f'{new[2]}\nОписание: {new[3]}')

async def place_menu(message: types.Message):
    places = database.database.loc_read()
    for place in places:
        await bot.send_venue(message.from_user.id,
                             latitude=place[1],
                             longitude=place[2],
                             title=place[3],
                             address=place[4],
                             foursquare_id=place[5])


# Выводит расписание преподавателей
async def schedule(message: types.Message):
    if not database.database.schedule_status():
        database.database.schedule_create()
    schedule_data = database.database.schedule_read()
    result_text = '\n'.join((f'{schedule_data[i][2]} - {schedule_data[i][3]}' for i in range(7)))
    await bot.send_message(message.from_user.id, text=result_text)

async def plan_ex(message: types.Message):
    if not database.database.plan_ex_status():
        database.database.plan_ex_create()
    plan_ex_data = database.database.plan_ex_read()
    day = datetime.datetime.today().weekday()
    result_text = f"{plan_ex_data[day][2]}: {plan_ex_data[day][3]}"
    await bot.send_message(message.from_user.id, text=result_text)

# Выводит Нормативы
async def exercise_standards(message: types.Message):
    await asyncio.sleep(0.3)
    if not database.database.ex_stand_status():
        database.database.ex_stand_create()
    ex_stand = database.database.ex_stand_read()
    try:
        await bot.send_photo(chat_id=message.from_user.id, photo=ex_stand[0][2], caption=ex_stand[0][3])
    except Exception:
        await bot.send_message(chat_id=message.from_user.id, text=' нормативы не загружены')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start,
                                CommandStart(),
                                state=None)
    dp.register_message_handler(news_menu,
                                text='🆕 новости',
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(schedule,
                                Text('📝 расписание'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(plan_ex,
                                Text('План занятия'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(exercise_standards,
                                Text('🏃 нормативы'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(place_menu,
                                Text('🚩 места занятий'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
