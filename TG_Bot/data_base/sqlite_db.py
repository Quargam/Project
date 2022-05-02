import sqlite3 as sq
from create_bot import dp, bot

def sql_start():
    global base, cur
    base = sq.connect('event_sport.db') # Подключение к БД сабытий
    cur = base.cursor() # Курсор БД событий
    baseU = sq.connect('Users_db.db') # Подключение к БД пользователей
    if base:
        print('Data base_menu connected OK!')
    # создание БД событий событий
    base.execute("""CREATE TABLE IF NOT EXISTS event(
                                                    img TEXT, 
                                                    name TEXT, 
                                                    description TEXT)
                                                    """)
    base.commit()
    # создание ДБ с точками на карте
    base.execute("""CREATE TABLE IF NOT EXISTS place(
                                                    location TEXT, 
                                                    title TEXT,
                                                    address TEXT)
                                                    """)
    base.commit()
    if baseU:
        print('Data base_users connected OK!')
    #  создание таблицу пользователей в БД
    baseU.execute("""CREATE TABLE IF NOT EXISTS users(
                                                    id INTEGER,
                                                    user_id INTEGER PRIMARY KEY,
                                                    active INTEGER DEFAULT 1
                                                    )""")
    baseU.commit()
    if baseU:
        print('Data base_admins connected OK!')
    #  создание таблицу админов в БД
    baseU.execute("""CREATE TABLE IF NOT EXISTS admins(
                                                    id INTEGER,
                                                    user_id INTEGER PRIMARY KEY,
                                                    active INTEGER DEFAULT 1
                                                    )""")
    baseU.commit()

# загрузка в БД информации про мероприятие
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO event VALUES (?,?,?)', tuple(data.values()))
        base.commit()

async def sql_add_place_command(data):
    async with state.proxy() as data:
        cur.execute('INSERT INTO event VALUES (?,?,?)', tuple(data.values()))
        base.commit()

# Отправка в виде сообщения о всех мероприятиях в БД
async def sql_read(message):
    for ret in cur.execute('SELECT * FROM event').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}')

# получение информации о всех мероприятиях из БД
async def sql_read2():
    return cur.execute('SELECT * FROM event').fetchall()

# удаление мероприятие из БД
async def sql_delete_command(name):
    cur.execute('DELETE FROM event WHERE name == ?', (name,))
    base.commit()