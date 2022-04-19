from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import admin_kb
from data_base import sqlite_db, db

db_users = db.Database_users("Users_db.db") # объект для управления users в БД

class FSMAdmin(StatesGroup): # Машины состояний
    photo = State()
    name = State()
    description = State()


# Получить ID текущего модератора
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    await message.delete()
    if not db_users.user_exists(message.from_user.id, 'admins'): # проверка отсутствия пользователя в таблице админов
        db_users.add_user(message.from_user.id, 'admins') # добавления пользователя в тоблицу админов
        await bot.send_message(message.from_user.id, 'добавлен в базу данных админов')
    if db_users.user_exists(message.from_user.id, 'admins'): # проверка пользователя в таблице админов
        await bot.send_message(message.from_user.id, 'Что хозяин надо??', reply_markup=admin_kb.button_case_admin)


# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if db_users.user_exists(message.from_user.id, 'admins'):
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Теперь введи название")


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Введи описание")


# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await sqlite_db.sql_add_command(state)
    await bot.send_message(message.from_user.id, 'команда успешно выполнена')
    await state.finish()

# Выход из состояния
# @dp.message_handler(state='*',commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')
    await message.delete()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


# @dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if db_users.user_exists(message.from_user.id, 'admins'):
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n описание: {ret[2]}\n Цена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                   add(InlineKeyboardButton(f'удалить {ret[1]}', callback_data=f'del {ret[1]}')))
    await message.delete()


@dp.message_handler(commands=['sendall'])
async def command_sendall(message: types.Message):
    if message.chat.type == 'private':
        if db_users.user_exists(message.from_user.id, 'admins'):
            text = message.text[9:]
            users = db_users.get_users()
            print(users)
            for row in users:
                try:
                    await bot.send_message(row[1], text, disable_notification=True)
                    if int(row[1]) != 1:
                        db_users.set_active(row[1], 1)
                except:
                    db_users.set_active(row[1], 0)
            await bot.send_message(message.from_user.id, 'успешная рассылка')
    await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Загрузить', state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    # dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands=['Удалить'])
