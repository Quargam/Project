from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Float
from aiogram import types
from create_bot import bot

days_val = {0: "пн", 1: "вт", 2: "ср", 3: "чт", 4: "пт", 5: "сб", 6: "вс"}


class Database:
    def __init__(self, engine, meta):
        self.engine = engine
        self.meta = meta
        self.conn = self.engine.connect()
        self.students = Table(
            'students', self.meta,
            Column('id', Integer, primary_key=True),
            Column('user_id', Integer),
            Column('first_name', String),
            Column('active', Boolean),
        )
        self.schedule = Table(
            'schedule', self.meta,
            Column('id', Integer, primary_key=True),
            Column('day_id', Integer),
            Column('day', String),
            Column('text', String),
        )
        self.ex_stand = Table(
            'ex_stand', self.meta,
            Column('id', Integer, primary_key=True),
            Column('specialty', String),
            Column('photo', String),
            Column('text', String),
        )
        self.news = Table(
            'news', self.meta,
            Column('id', Integer, primary_key=True),
            Column('photo', String),
            Column('name', String),
            Column('description', String),
        )
        self.location = Table(
            'location', self.meta,
            Column('id', Integer, primary_key=True),
            Column('latitude', Float),
            Column('longitude', Float),
            Column('title', String),
            Column('address', String),
            Column('foursquare_id', String),
        )
        self.plan_ex = Table(
            'plan_ex', self.meta,
            Column('id', Integer, primary_key=True),
            Column('day_id', Integer),
            Column('day', String),
            Column('text', String),
        )
        self.id_chat = Table(
            'id_chat', self.meta,
            Column('id', Integer, primary_key=True),
            Column('ID_group', Integer),
            Column('ID_chat', Integer),
        )
        self.admins = Table(
            'admins', self.meta,
            # Column('id', Integer, primary_key=True),
            Column('user_id', Integer, primary_key=True),
            Column('first_name', String),
            Column('active', Boolean),
        )
        self.meta.create_all(engine)

    def id_chat_status(self):
        select = self.id_chat.select()
        result = self.conn.execute(select).fetchall()
        return bool(len(result))

    def id_chat_read(self):
        select = self.id_chat.select()
        result = self.conn.execute(select).fetchall()
        return result

    def id_chat_update(self, message: types.Message):
        self.conn.execute(self.id_chat.update().where(self.id_chat.c.id == 1).values(
            ID_group=int(message.sender_chat.id),
            ID_chat=int(message.chat.id),
        ))

    def id_chat_del(self, message: types.Message):
        self.conn.execute(self.id_chat.update().where(self.id_chat.c.id == 1).values(
            ID_group=None,
            ID_chat=None,
        ))

    def id_chat_create(self):
        insert = self.id_chat.insert().values(
            ID_group=None,
            ID_chat=None,
        )
        self.conn.execute(insert)

    def student_exist(self, message: types.Message):
        select = self.students.select().where(self.students.c.user_id == message.from_user.id)
        result = self.conn.execute(select).fetchall()
        return bool(len(result))

    def student_add(self, message: types.Message):
        insert = self.students.insert().values(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            active=True,
        )
        self.conn.execute(insert)

    def student_read(self):
        select = self.students.select()
        result = self.conn.execute(select).fetchall()
        return result

    def admin_exist(self, message: types.Message):
        select = self.admins.select().where(self.admins.c.user_id == message.from_user.id)
        result = self.conn.execute(select).fetchall()
        return bool(len(result))

    def admin_add(self, admin: list):
        insert = self.admins.insert().values(
            user_id=admin['user']['id'],
            first_name=admin['user']['first_name'],
            active=True,
        )
        self.conn.execute(insert)

    def admin_read(self):
        select = self.admins.select()
        result = self.conn.execute(select).fetchall()
        return result

    def student_active(self, student_id):
        """
        код который нигде не участвует
        """
        self.conn.execute(self.students.update().where(self.students.c.id == student_id).values(active=True))

    def schedule_status(self):
        select = self.schedule.select()
        result = self.conn.execute(select).fetchall()
        return bool(len(result))

    def schedule_update(self, data):
        self.conn.execute(self.schedule.update().where(self.schedule.c.day_id == int(data['day_id'])).values(text=data['text']))

    def schedule_create(self):
        for i in range(7):
            insert = self.schedule.insert().values(
                day_id=i,
                day=days_val[i],
                text='None',
            )
            self.conn.execute(insert)

    def schedule_read(self):
        select = self.schedule.select()
        result = self.conn.execute(select).fetchall()
        return result

    def ex_stand_status(self):
        select = self.ex_stand.select()
        result = self.conn.execute(select).fetchall()
        return bool(len(result))

    def ex_stand_read(self):
        select = self.ex_stand.select()
        result = self.conn.execute(select).fetchall()
        return result

    def ex_stand_create(self):
        insert = self.ex_stand.insert().values(
            specialty='hockey',
            photo=None,
            text="None",
        )
        self.conn.execute(insert)

    def ex_stand_update(self, data):
        self.conn.execute(self.ex_stand.update().\
                          where(self.ex_stand.c.specialty == 'hockey').values(photo=data['photo_exercise_standards']),
                          text=data['text_exercise_standards'],
                          )

    def news_read(self):
        select = self.news.select()
        result = self.conn.execute(select).fetchall()
        return result

    def news_add(self, data):
        insert = self.news.insert().values(
            photo=data['photo'],
            name=data['name'],
            description=data['description'],
        )
        self.conn.execute(insert)

    def news_del(self, name):
        delete = self.news.delete().where(self.news.c.name == name)
        self.conn.execute(delete)

    def loc_read(self):
        select = self.location.select()
        result = self.conn.execute(select).fetchall()
        return result

    def loc_add(self, data):
        insert = self.location.insert().values(
            latitude=data['latitude'],
            longitude=data['longitude'],
            title=data['title'],
            address=data['address'],
            foursquare_id=data['foursquare_id'],
        )
        self.conn.execute(insert)

    def loc_del(self, title):
        delete = self.location.delete().where(self.location.c.title == title)
        self.conn.execute(delete)

    def plan_ex_status(self):
        select = self.plan_ex.select()
        result = self.conn.execute(select).fetchall()
        return bool(len(result))

    def plan_ex_update(self, data):
        self.conn.execute(self.plan_ex.update().where(self.plan_ex.c.day_id == int(data['day_id'])).values(text=data['text']))

    def plan_ex_create(self):
        for i in range(7):
            insert = self.plan_ex.insert().values(
                day_id=i,
                day=days_val[i],
                text='None',
            )
            self.conn.execute(insert)

    def plan_ex_read(self):
        select = self.plan_ex.select()
        result = self.conn.execute(select).fetchall()
        return result

engine = create_engine('sqlite:///database.db', echo=False)
meta = MetaData()
database = Database(engine=engine, meta=meta)


async def add_admins():
    try:
        admins = await bot.get_chat_administrators(database.id_chat_read()[0][1])
        for admin in admins:
            print(admin['user'])
            database.admin_add(admin)
    except Exception as exc:
        print(f'add_admins: что-то не получилось - {exc}')


def first_set_config():
    if not database.id_chat_status():
        database.id_chat_create()

