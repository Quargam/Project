from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import admin_kb
from data_base import sqlite_db, db
import ast
import datetime
import zoneinfo
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # для отправки сообщений в определенное время асинхр
from aiogram.dispatcher.filters import ChatTypeFilter, Text, AdminFilter, ContentTypeFilter, Command

db_users = db.Database_users("Users_db.db")  # объект для управления users в БД
scheduler = AsyncIOScheduler()
TimerFlag = False
Days = {0: "пн", 1: "вт", 2: "ср", 3: "чт", 4: "пт", 5: "сб", 6: "вс"}
with open("ID_chat.json", "r") as ID_chat_json:
    ID_chat = json.load(ID_chat_json)

class FSM_generic(StatesGroup):  # Машины состояний
    Step_event_0 = State()
    Step_event_1 = State()
    Step_event_2 = State()
    Step_sendall_0 = State()
    Step_exercise_standards_0 = State()
    Step_exercise_standards_1 = State()
    Step_place_0 = State()
    Step_place_1 = State()
    Step_place_2 = State()


async def make_changes_command(message: types.Message):
    """
    передает модератору группы клавиатуру админа
    """
    await message.reply('OK', reply_markup=admin_kb.button_case_admin)


# Начало диалога загрузки нового пункта мероприятия
async def cm_start(message: types.Message):
    if db_users.user_exists(message.from_user.id, 'admins'):
        await FSM_generic.Step_event_0.set()
        await message.reply('Загрузи фото', reply_markup=admin_kb.button_case_admin_with_but_cancel)


# Ловим первый ответ и пишем в словарь
async def load_photo(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['Step_event_0'] = message.photo[0].file_id
    await FSM_generic.Step_event_1.set()
    await message.reply("Теперь введи название")


# Ловим второй ответ
async def load_name(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['Step_event_1'] = message.text
    await FSM_generic.Step_event_2.set()
    await message.reply("Введи описание")


# Ловим третий ответ
async def load_description(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['Step_event_2'] = message.text
    await sqlite_db.sql_add_command(state)
    await bot.send_message(message.from_user.id, 'команда успешно выполнена', reply_markup=admin_kb.button_case_admin)
    await state.finish()


# Выход из состояния
async def cancel_handler(message: types.Message, state: FSM_generic):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply('NOT OK', reply_markup=admin_kb.button_case_admin)
        return
    await state.finish()
    await message.reply('OK', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# удаления пункта мероприятия
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_event '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del_event ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del_event ", "")} удалена.', show_alert=True)


# @dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    read = await sqlite_db.sql_read2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n описание: {ret[2]}')
        await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(f'удалить {ret[1]}', callback_data=f'del_event {ret[1]}')))


# отправить сообщение всем пользователям в БД
async def command_sendall(message: types.Message):
    await FSM_generic.Step_sendall_0.set()
    await message.reply('Напишите текст который хотите всем отправить',
                        reply_markup=admin_kb.button_case_admin_with_but_cancel)


async def sendall(message: types.Message, state: FSM_generic):
    text = message.text
    users = db_users.get_users(table='users')
    for row in users:
        try:
            await bot.send_message(row[1], text, disable_notification=True)
            if int(row[2]) != 1:
                db_users.set_active(row[1], active=1, table='users')
        except:
            db_users.set_active(row[1], active=0, table='users')
    await bot.send_message(message.from_user.id, 'успешная рассылка', reply_markup=admin_kb.button_case_admin)
    await state.finish()


# Команда чтобы загрузить нормативы
async def exercise_standards_admin(message: types.Message):
    if db_users.user_exists(message.from_user.id, 'admins'):
        await FSM_generic.Step_exercise_standards_0.set()
        await message.reply('Загрузите фото нормативов', reply_markup=admin_kb.button_case_admin_with_but_cancel)


async def exercise_standards_photo(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['photo_exercise_standards'] = message.photo[0].file_id
    await FSM_generic.Step_exercise_standards_1.set()
    await message.reply("Теперь введи описание нормативов")


async def exercise_standards_text(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['text_exercise_standards'] = message.text
    await state.finish()
    with open('exercise_standards.json', 'w') as exercise_standards_json:
        json.dump(data.as_dict(), exercise_standards_json)
    await bot.send_message(message.from_user.id, 'Команда выполнена', reply_markup=admin_kb.button_case_admin)


# Команда чтобы загрузить локацию
# @dp.message_handler(commands=['Загрузить_геопозицию'], state=None)
async def place_admin(message: types.Message):
    if db_users.user_exists(message.from_user.id, 'admins'):
        await FSM_generic.Step_place_0.set()
        await message.reply('отправьте геопозицию', reply_markup=admin_kb.button_case_admin_with_but_cancel)


async def place_location(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['Step_place_0'] = str(message.location)
    await FSM_generic.Step_place_1.set()
    await message.reply("Теперь введи название геопозиции")


async def place_title(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['Step_place_1'] = message.text
    await FSM_generic.Step_place_2.set()
    await message.reply("Теперь введи адрес геопозиции")


async def place_address(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['Step_place_2'] = message.text
    await sqlite_db.sql_add_place_command(state)
    await state.finish()
    await message.reply("геолокация успешна согранена", reply_markup=admin_kb.button_case_admin)


# удаления пункта геопозиции
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_place '))
async def del_callback_place(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del_place ', ''), name='title', table='place')
    await callback_query.answer(text=f'{callback_query.data.replace("del_place ", "")} удалена.', show_alert=True)


# @dp.message_handler(commands='Удалить_геопозицию')
async def delete_item_place(message: types.Message):
    read = await sqlite_db.sql_read2(name='place')
    for ret in read:
        await bot.send_venue(message.from_user.id, latitude=ast.literal_eval(ret[0])["latitude"],
                             longitude=ast.literal_eval(ret[0])["longitude"],
                             title=ret[1], address=ret[2])
        await bot.send_message(message.from_user.id, text='^^^',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'удалить {ret[1]}',
                                callback_data=f'del_place {ret[1]}')))


# отправляет сообщение с учетом расписания и дня недели
async def send_channel():
    global ID_chat
    if datetime.datetime.today().weekday() <= 5:
        with open("schedule.json", "r", encoding='utf-8') as schedule_json:
            res_dict = json.load(schedule_json)
        await bot.send_message(chat_id=int(ID_chat["ID_group"]),
                               text='хоккей ' + Days[datetime.datetime.today().weekday()] + '\n' +
                                    str(datetime.datetime.now())[0:16] + '\n' +
                                    res_dict[str(datetime.datetime.today().weekday())] +
                                    '\n 0 человек',
                               parse_mode=None,
                               disable_notification=True)
    else:
        pass


# запускает отправку сообщений к конфу каждые 10 сек
def timer():
    global scheduler
    # scheduler.add_job(send_channel, 'interval', seconds=10)
    scheduler.add_job(send_channel, 'cron', day_of_week='mon-sat', hour=9, minute=0)
    scheduler.add_job(send_channel, 'cron', day_of_week='mon-sat', hour=10, minute=45)
    # scheduler.add_job(send_channel, 'cron', day_of_week='mon-sat', hour=12, minute=20)
    scheduler.add_job(send_channel, 'cron', day_of_week='mon-sat', hour=13, minute=55)
    scheduler.add_job(send_channel, 'cron', day_of_week='mon-sat', hour=15, minute=30)
    scheduler.add_job(send_channel, 'cron', day_of_week='mon-sat', hour=17, minute=5)
    scheduler.start()


# включает таймер
async def start_timer(message: types.Message):
    global TimerFlag
    if TimerFlag is False:
        await message.answer('timer start \n в группу будет отправлять сообщение каждые 10 секунд\n '
                             'частоту и период отправки можно настраивать')
        timer()
        TimerFlag = True
    else:
        await message.answer('timer is running')


# выключает таймер
async def off_timer(message: types.Message):
    global TimerFlag, scheduler
    if TimerFlag is False:
        pass
    else:
        scheduler.shutdown(wait=False)
        TimerFlag = False


# команды к функциям
def register_handlers_admins(dp: Dispatcher):
    dp.register_message_handler(make_changes_command,
                                Command('модератор'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
    dp.register_message_handler(cancel_handler,
                                Text('⬅️❌ Отмена'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state='*')
    dp.register_message_handler(cm_start,
                                Text('⬇️🆕 Загрузить новости'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
    dp.register_message_handler(load_photo,
                                ContentTypeFilter('photo'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_event_0)
    dp.register_message_handler(load_name,
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_event_1)
    dp.register_message_handler(load_description,
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_event_2)
    dp.register_message_handler(delete_item,
                                Text('❌🆕 Удалить новость'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
    dp.register_message_handler(exercise_standards_admin,
                                Text('⬇🏃 Загрузить нормативы'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
    dp.register_message_handler(exercise_standards_photo,
                                ContentTypeFilter('photo'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_exercise_standards_0)
    dp.register_message_handler(exercise_standards_text,
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_exercise_standards_1)
    dp.register_message_handler(command_sendall,
                                Text('📢 Рассылка'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
    dp.register_message_handler(sendall,
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_sendall_0)
    dp.register_message_handler(place_admin,
                                Text('⬇🚩 Загрузить геопозицию'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
    dp.register_message_handler(delete_item_place,
                                Text('❌🚩 Удалить геопозицию'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
    dp.register_message_handler(place_location,
                                ContentTypeFilter('location'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_place_0)
    dp.register_message_handler(place_title,
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_place_1)
    dp.register_message_handler(place_address,
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=FSM_generic.Step_place_2)
    dp.register_message_handler(start_timer,
                                Text('⏲✅ ️Включить отправку сообщений в группу'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
    dp.register_message_handler(off_timer,
                                Text('⏲️❌ Выключить отправку сообщений в группу'),
                                ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                                AdminFilter(is_chat_admin=int(ID_chat["ID_chat"])),
                                state=None)
