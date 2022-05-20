import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import admin_kb
from data_base import database
import datetime
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # для отправки сообщений в определенное время асинхр
from aiogram.dispatcher.filters import Text, Command
from Filter import IsPrivate, IsUserAdmin

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
    Step_place_loc_1 = State()
    Step_place_loc_2 = State()
    Step_exercise_standards_load_0 = State()
    Step_plan_ex_load_0 = State()


@dp.message_handler(lambda message: message.sender_chat.type == 'channel', commands=['set'])
async def set_config(message: types.Message):
    """
    Пишите в канале команду /set и бот запонимает id канала и чата.
    После бот будет знать админов канала и чата
    """
    database.database.id_chat_update(message)
    await message.delete()


async def make_changes_command(message: types.Message):
    """
    передает модератору клавиатуру админа
    Так как я не знаю как отслеживать изменения статуса админов, то просто каждый раз и обновляю их список
    !нужно узнать как это сделать на 2.* версии aiogram!
    """
    database.database.admin_del_all()
    await database.database.add_admins()
    await message.reply('OK', reply_markup=admin_kb.button_case_admin)


async def news_start(message: types.Message):
    await FSM_generic.Step_event_0.set()
    await message.reply('Загрузи фото', reply_markup=admin_kb.button_case_admin_with_but_cancel)


async def load_photo(message: types.Message, state: FSM_generic):
    await state.update_data(photo=message.photo[0].file_id)
    await FSM_generic.Step_event_1.set()
    await message.reply("Теперь введи название")


async def load_name(message: types.Message, state: FSM_generic):
    await state.update_data(name=message.text)
    await FSM_generic.Step_event_2.set()
    await message.reply("Введи описание")


async def load_description(message: types.Message, state: FSM_generic):
    await state.update_data(description=message.text)
    data = await state.get_data()
    database.database.news_add(data)
    await bot.send_message(message.from_user.id, 'команда успешно выполнена', reply_markup=admin_kb.button_case_admin)
    await state.finish()


async def cancel_handler(message: types.Message, state: FSM_generic):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply('NOT OK', reply_markup=admin_kb.button_case_admin)
        return
    await state.finish()
    await message.reply('OK', reply_markup=admin_kb.button_case_admin)
    await message.delete()


@dp.callback_query_handler(admin_kb.item_callback.filter(item_name="news"))
async def news_del_callback(call: types.CallbackQuery, callback_data: dict):
    """
    происходить что-то не здоровое:
    aiogram.utils.exceptions.RetryAfter: Flood control exceeded. Retry in 9 seconds.
    [!]разобраться потом[!]
    но вроде работает
    """
    database.database.news_del(callback_data['name'])
    await call.answer(text=f'{callback_data["name"]} удалена.', show_alert=True)


async def news_del(message: types.Message):
    news_data = database.database.news_read()
    for new in news_data:
        await bot.send_photo(message.from_user.id, new[1], f'{new[2]}\nОписание: {new[3]}')
        await bot.send_message(message.from_user.id,
                               text='^^^',
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton(f'удалить {new[2]}',
                                                        callback_data=admin_kb.item_callback.new(
                                                            item_name="news",
                                                            name=new[2]
                                                        ))))


async def command_sendall(message: types.Message):
    await FSM_generic.Step_sendall_0.set()
    await message.reply('Напишите текст который хотите всем отправить',
                        reply_markup=admin_kb.button_case_admin_with_but_cancel)


async def sendall(message: types.Message, state: FSM_generic):
    students = database.database.student_read()
    for student in students:
        try:
            await bot.send_message(student[1], message.text, disable_notification=True)
        except:
            pass
    await bot.send_message(message.from_user.id, 'успешная рассылка', reply_markup=admin_kb.button_case_admin)
    await state.finish()


async def markup_schedule(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    for i in range(7):
        button = InlineKeyboardButton(f'изменить {Days[i]}', callback_data=admin_kb.item_callback.new(
            item_name="schedule",
            name=i
            ))
        markup.insert(button)
    await bot.send_message(message.from_user.id, text='Выберите что хотите изменить:', reply_markup=markup)

@dp.callback_query_handler(admin_kb.item_callback.filter(item_name="schedule"))
async def schedule_callback(call: types.CallbackQuery, callback_data: dict, state: FSM_generic):
    await call.answer(cache_time=15)
    await call.message.answer(text=f'{Days[int(callback_data["name"])]}: напишите ФИО ',
                              reply_markup=admin_kb.button_case_admin_with_but_cancel)
    await FSM_generic.Step_exercise_standards_load_0.set()
    await state.update_data(day_id=callback_data['name'])

async def load_schedule(message: types.Message, state: FSM_generic):
    await state.update_data(text=message.text)
    data = await state.get_data()
    database.database.schedule_update(data)
    await bot.send_message(message.from_user.id, 'Команда выполнена', reply_markup=admin_kb.button_case_admin)
    await state.finish()

async def exercise_standards_admin(message: types.Message):
    await FSM_generic.Step_exercise_standards_0.set()
    await message.reply('Загрузите фото нормативов', reply_markup=admin_kb.button_case_admin_with_but_cancel)


async def exercise_standards_photo(message: types.Message, state: FSM_generic):
    await FSM_generic.Step_exercise_standards_1.set()
    await state.update_data(photo_exercise_standards=message.photo[0].file_id)
    await message.reply("Теперь введи описание нормативов")


async def exercise_standards_text(message: types.Message, state: FSM_generic):
    await state.update_data(text_exercise_standards=message.text)
    data = await state.get_data()
    database.database.ex_stand_update(data)
    await bot.send_message(message.from_user.id, 'Команда выполнена', reply_markup=admin_kb.button_case_admin)
    await state.finish()


async def place_admin(message: types.Message):
    await FSM_generic.Step_place_0.set()
    await message.reply('отправьте геопозицию или место', reply_markup=admin_kb.button_case_admin_with_but_cancel)


async def place_location(message: types.Message, state: FSM_generic):
    if message.venue:
        await state.update_data(latitude=message.venue.location.latitude)
        await state.update_data(longitude=message.venue.location.longitude)
        await state.update_data(title=message.venue.title)
        await state.update_data(address=message.venue.address)
        await state.update_data(foursquare_id=message.venue.foursquare_id)
        data = await state.get_data()
        database.database.loc_add(data)
        await message.reply("место успешна сохранено", reply_markup=admin_kb.button_case_admin)
        await state.finish()
    else:
        await state.update_data(latitude=message.location.latitude)
        await state.update_data(longitude=message.location.longitude)
        await FSM_generic.Step_place_loc_1.set()
        await message.reply("Теперь введи название геопозиции")


async def place_title(message: types.Message, state: FSM_generic):
    await state.update_data(title=message.text)
    await FSM_generic.Step_place_loc_2.set()
    await message.reply("Теперь введи адрес геопозиции")


async def place_address(message: types.Message, state: FSM_generic):
    await state.update_data(address=message.text)
    await state.update_data(foursquare_id=None)
    data = await state.get_data()
    database.database.loc_add(data)
    await message.reply("геолокация успешна сохранена", reply_markup=admin_kb.button_case_admin)
    await state.finish()


@dp.callback_query_handler(admin_kb.item_callback.filter(item_name="places"))
async def loc_del_callback(call: types.CallbackQuery, callback_data: dict):
    database.database.loc_del(callback_data['name'])
    await call.answer(text=f'{callback_data["name"]} удалена.', show_alert=True)


async def delete_item_place(message: types.Message):
    places = database.database.loc_read()
    for place in places:
        await bot.send_venue(message.from_user.id,
                             latitude=place[1],
                             longitude=place[2],
                             title=place[3],
                             address=place[4],
                             foursquare_id=place[5])
        await bot.send_message(message.from_user.id,
                               text='^^^',
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton(f'удалить {place[3]}',
                                                        callback_data=admin_kb.item_callback.new(
                                                            item_name="places",
                                                            name=place[3]
                                                        ))))

async def plan_ex_all(message: types.Message):
    if not database.database.plan_ex_status():
        database.database.plan_ex_create()
    plan_ex_data = database.database.plan_ex_read()
    result_text = '\n'.join((f'{plan_ex_data[i][2]} - {plan_ex_data[i][3]}' for i in range(7)))
    await bot.send_message(message.from_user.id, text=result_text)

async def markup_plan_ex_all(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    for i in range(7):
        button = InlineKeyboardButton(f'изменить {Days[i]}', callback_data=admin_kb.item_callback.new(
            item_name="plan_ex",
            name=i
            ))
        markup.insert(button)
    await bot.send_message(message.from_user.id, text='[план занятия]\nВыберите что хотите изменить:', reply_markup=markup)

@dp.callback_query_handler(admin_kb.item_callback.filter(item_name="plan_ex"))
async def plan_ex_callback(call: types.CallbackQuery, callback_data: dict, state: FSM_generic):
    await call.answer(cache_time=15)
    await call.message.answer(text=f'{Days[int(callback_data["name"])]}: Напишите план занятий на сегодня',
                              reply_markup=admin_kb.button_case_admin_with_but_cancel)
    await FSM_generic.Step_plan_ex_load_0.set()
    await state.update_data(day_id=callback_data['name'])

async def load_plan_ex(message: types.Message, state: FSM_generic):
    await state.update_data(text=message.text)
    data = await state.get_data()
    database.database.plan_ex_update(data)
    await bot.send_message(message.from_user.id, 'Команда выполнена', reply_markup=admin_kb.button_case_admin)
    await state.finish()

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


async def start_timer(message: types.Message):
    global TimerFlag
    if TimerFlag is False:
        await message.answer('timer start \n в группу будет отправлять сообщение каждые 10 секунд\n '
                             'частоту и период отправки можно настраивать')
        timer()
        TimerFlag = True
    else:
        await message.answer('timer is running')


async def off_timer():
    global TimerFlag, scheduler
    if TimerFlag is False:
        pass
    else:
        scheduler.shutdown(wait=False)
        TimerFlag = False


def register_handlers_admins(dp: Dispatcher):
    dp.register_message_handler(make_changes_command,
                                IsUserAdmin(),
                                Command('модератор'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(cancel_handler,
                                IsUserAdmin(),
                                Text('⬅️❌ Отмена'),
                                chat_type=types.ChatType.PRIVATE,
                                state='*')
    dp.register_message_handler(news_start,
                                IsPrivate(),
                                IsUserAdmin(),
                                Text('⬇️🆕 Загрузить новости'),
                                state=None)
    dp.register_message_handler(load_photo,
                                IsUserAdmin(),
                                content_types=['photo'],
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_event_0)
    dp.register_message_handler(load_name,
                                IsUserAdmin(),
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_event_1)
    dp.register_message_handler(load_description,
                                IsUserAdmin(),
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_event_2)
    dp.register_message_handler(news_del,
                                IsUserAdmin(),
                                Text('❌🆕 Удалить новость'),
                                chat_type=types.ChatType.PRIVATE,\
                                state=None)
    dp.register_message_handler(markup_schedule,
                                IsUserAdmin(),
                                Text('⬇📝Изменить расписание'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(load_schedule,
                                IsUserAdmin(),
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_exercise_standards_load_0)
    dp.register_message_handler(plan_ex_all,
                                IsUserAdmin(),
                                Text('Планы занятий'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(markup_plan_ex_all,
                                IsUserAdmin(),
                                Text('Изменить план занятия'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(load_plan_ex,
                                IsUserAdmin(),
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_plan_ex_load_0)
    dp.register_message_handler(exercise_standards_admin,
                                IsUserAdmin(),
                                Text('⬇🏃 Загрузить нормативы'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(exercise_standards_photo,
                                IsUserAdmin(),
                                content_types=['photo'],
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_exercise_standards_0)
    dp.register_message_handler(exercise_standards_text,
                                IsUserAdmin(),
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_exercise_standards_1)
    dp.register_message_handler(command_sendall,
                                IsUserAdmin(),
                                Text('📢 Рассылка'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(sendall,
                                chat_type=types.ChatType.PRIVATE,
                                # is_chat_admin=int(ID_chat["ID_chat"]),
                                state=FSM_generic.Step_sendall_0)
    dp.register_message_handler(place_admin,
                                IsUserAdmin(),
                                Text('⬇🚩 Загрузить геопозицию'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(delete_item_place,
                                IsUserAdmin(),
                                Text('❌🚩 Удалить геопозицию'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(place_location,
                                IsUserAdmin(),
                                content_types=['location', 'venue'],
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_place_0)
    dp.register_message_handler(place_title,
                                IsUserAdmin(),
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_place_loc_1)
    dp.register_message_handler(place_address,
                                chat_type=types.ChatType.PRIVATE,
                                state=FSM_generic.Step_place_loc_2)
    dp.register_message_handler(start_timer,
                                IsUserAdmin(),
                                Text('⏲✅ ️Включить отправку сообщений в группу'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
    dp.register_message_handler(off_timer,
                                IsUserAdmin(),
                                Text('⏲️❌ Выключить отправку сообщений в группу'),
                                chat_type=types.ChatType.PRIVATE,
                                state=None)
