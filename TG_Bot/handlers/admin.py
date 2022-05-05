from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import admin_kb
from data_base import sqlite_db, db
import ast
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler # для отправки сообщений в определенное время асинхр

db_users = db.Database_users("Users_db.db")  # объект для управления users в БД
scheduler = AsyncIOScheduler()
TimerFlag = False
Days = {0: "пн", 1: "вт", 2: "ср", 3: "чт", 4: "пт", 5: "сб", 6: "вс"}


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


# Получить ID текущего модератора
async def make_changes_command(message: types.Message):
    await message.delete()
    if not db_users.user_exists(message.from_user.id, 'admins'):  # проверка отсутствия пользователя в таблице админов
        db_users.add_user(message.from_user.id, 'admins')  # добавления пользователя в тоблицу админов
        await bot.send_message(message.from_user.id, 'добавлен в базу данных админов')
    if db_users.user_exists(message.from_user.id, 'admins'):  # проверка пользователя в таблице админов
        await bot.send_message(message.from_user.id, 'Что хозяин надо??', reply_markup=admin_kb.button_case_admin)


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
    # print(tuple(data.values()))
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
    if db_users.user_exists(message.from_user.id, 'admins'):
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n описание: {ret[2]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                   add(InlineKeyboardButton(f'удалить {ret[1]}', callback_data=f'del_event {ret[1]}')))
    await message.delete()


# отправить сообщение всем пользователям в БД
async def command_sendall(message: types.Message):
    if db_users.user_exists(message.from_user.id, 'admins'):
        await FSM_generic.Step_sendall_0.set()
        await message.reply('Напишите текст который хотите всем отправить',
                            reply_markup=admin_kb.button_case_admin_with_but_cancel)

async def sendall(message: types.Message, state: FSM_generic):
    if message.chat.type == 'private':
        text = message.text
        if db_users.user_exists(message.from_user.id, 'admins') and text != '/Отмена':
            users = db_users.get_users(table='users')
            for row in users:
                try:
                    await bot.send_message(row[1], text, disable_notification=True)
                    if int(row[2]) != 1:
                        db_users.set_active(row[1], active=1, table='users')
                except:
                    db_users.set_active(row[1], active=0, table='users')
            await bot.send_message(message.from_user.id, 'успешная рассылка', reply_markup=admin_kb.button_case_admin)
        elif text == '/Отмена':
            await bot.send_message(message.from_user.id, 'Отмена', reply_markup=admin_kb.button_case_admin)
    await state.finish()
    await message.delete()


# Команда чтобы загрузить нормативы
async def exercise_standards_admin(message: types.Message):
    if db_users.user_exists(message.from_user.id, 'admins'):
        await FSM_generic.Step_exercise_standards_0.set()
        await message.reply('Загрузите фото нормативов', reply_markup=admin_kb.button_case_admin_with_but_cancel)


async def exercise_standards_photo(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['Step_exercise_standards_0'] = message.photo[0].file_id
    await FSM_generic.Step_exercise_standards_1.set()
    await message.reply("Теперь введи описание нормативов")


async def exercise_standards_text(message: types.Message, state: FSM_generic):
    async with state.proxy() as data:
        data['Step_exercise_standards_1'] = message.text
    await state.finish()
    with open('exercise_standards.txt', 'w') as file:
        file.write(str(tuple(data.values())))
    await bot.send_message(message.from_user.id, 'Команда выполнена', reply_markup=admin_kb.button_case_admin)

# Команда чтобы загрузить локацию
@dp.message_handler(commands=['Загрузить_геопозицию'], state=None)
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
        # print(data)
    await sqlite_db.sql_add_place_command(state)
    await state.finish()
    await message.reply("геолокация успешна согранена", reply_markup=admin_kb.button_case_admin)

# удаления пункта геопозиции
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_place '))
async def del_callback_place(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del_place ', ''), name='title', table='place')
    await callback_query.answer(text=f'{callback_query.data.replace("del_place ", "")} удалена.', show_alert=True)


@dp.message_handler(commands='Удалить_геопозицию')
async def delete_item_place(message: types.Message):
    if db_users.user_exists(message.from_user.id, 'admins'):
        read = await sqlite_db.sql_read2(name='place')
        for ret in read:
            await bot.send_venue(message.from_user.id, latitude=ast.literal_eval(ret[0])["latitude"],
                                 longitude=ast.literal_eval(ret[0])["longitude"],
                                 title=ret[1], address=ret[2])
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                   add(InlineKeyboardButton(f'удалить {ret[1]}', callback_data=f'del_place {ret[1]}')))
    await message.delete()

# отправляет сообщение с учетом расписания и дня недели
async def send_channel():
    if datetime.datetime.today().weekday() <= 5:
        file = open("schedule.txt", encoding='utf-8')
        res_dict = ast.literal_eval(file.read())
        await bot.send_message(chat_id=int(open('ID_chat.txt').read()),
                               text='хоккей ' + Days[datetime.datetime.today().weekday()] + '\n' +
                               str(datetime.datetime.now())[0:16] + '\n' +
                               res_dict[str(datetime.datetime.today().weekday())],
                               parse_mode=None,
                               disable_notification=True)
    else:
        pass

# запускает отправку сообщений к конфу каждые 10 сек
def timer():
    global scheduler
    scheduler.add_job(send_channel, 'interval', seconds=10)
    scheduler.start()

# включает таймер
async def start_timer(message: types.Message):
    if message.chat["type"] == "private":
        global TimerFlag
        if TimerFlag is False:
            await message.answer('timer start \n в группу будет отправлять сообщение каждые 5 минут\n '
                                 'частоту и период отправки можно настраивать')
            timer()
            TimerFlag = True
        else:
            await message.answer('timer is running')
    else:
        pass

#выключает таймер
async def off_timer(message: types.Message):
    if message.chat["type"] == "private":
        global TimerFlag, scheduler
        if TimerFlag is False:
            pass
        else:
            scheduler.shutdown()
            TimerFlag = False
    else:
        pass

# команды к функциям
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['модератор'], is_chat_admin=True)
    dp.register_message_handler(cancel_handler, state='*', commands='Отмена')
    dp.register_message_handler(cm_start, commands='Загрузить_Мероприятие', state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSM_generic.Step_event_0)
    dp.register_message_handler(load_name, state=FSM_generic.Step_event_1)
    dp.register_message_handler(load_description, state=FSM_generic.Step_event_2)
    dp.register_message_handler(delete_item, commands=['Удалить_Мероприятие'])
    dp.register_message_handler(exercise_standards_admin, commands=['Загрузить_нормативы'], state=None)
    dp.register_message_handler(exercise_standards_photo, content_types=['photo'], state=FSM_generic.Step_exercise_standards_0)
    dp.register_message_handler(exercise_standards_text, state=FSM_generic.Step_exercise_standards_1)
    dp.register_message_handler(command_sendall, commands=['Рассылка'], state=None)
    dp.register_message_handler(sendall, state=FSM_generic.Step_sendall_0)
    dp.register_message_handler(place_admin, commands='Загрузить_геопозицию', state=None)
    dp.register_message_handler(place_location, content_types=['location'], state=FSM_generic.Step_place_0)
    dp.register_message_handler(place_title, state=FSM_generic.Step_place_1)
    dp.register_message_handler(place_address, state=FSM_generic.Step_place_2)
    dp.register_message_handler(start_timer, commands='Включить_регулярную_отправку_сообщений', state=None)
    dp.register_message_handler(off_timer, commands='Выключить_регулярную_отправку_сообщений', state=None)
