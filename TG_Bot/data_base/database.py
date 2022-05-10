from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Float
from aiogram import types

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
        self.meta.create_all(engine)

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

    def student_active(self, student_id):
        """
        код который нигде не участвует
        """
        self.conn.execute(self.students.update().where(self.students.c.id == student_id).values(active=True))

    def schedule_status(self):
        select = self.schedule.select()
        result = self.conn.execute(select).fetchall()
        return bool(len(result))

    def schedule_update(self, day_id, text):
        self.conn.execute(self.schedule.update().where(self.schedule.c.day_id == day_id).values(text=text))

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

engine = create_engine('sqlite:///database.db', echo=False)
meta = MetaData()
database = Database(engine=engine, meta=meta)
