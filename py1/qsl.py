import sqlite3

x = [['pasha', '1111'], ['pasha', '1111'], ['pasha', '1111'], ['pasha', '1111'], ['pasha', '1111'], ['pasha', '1111'],
     ['pasha', '1111'], ['pasha', '1111']]

base = sqlite3.connect('new.db')
cur = base.cursor()

# base.execute('CREATE TABLE IF NOT EXISTS {}(login PRIMARY KEY, password text)'.format('data'))
# base.commit()
#
# cur.execute('INSERT INTO data VALUES(?,?)', ('jonny123', '123456789'))
# base.commit()
# cur.execute('INSERT INTO data VALUES(?,?)', ('billy123', 'password'))
# base.commit()
# # cur.executemany('INSERT INTO date VALUES(?,?)', (x))
# # base.commit()

# r = cur.execute('SELECT login FROM data').fetchall()
# print(r)
#
# r = cur.execute('SELECT password FROM data WHERE  login  == ?', ('jonny123',)).fetchone()
# print(r)

# cur.execute('UPDATE data SET password == ? WHERE login  == ?', ('password', 'jonny123'))
# base.commit()


# cur.execute('UPDATE data SET password == ? WHERE password  == ?', ('1234', '1234567890'))
# base.commit()

# cur.execute('DELETE FROM data WHERE login == ?', ('jonny123',))
# base.commit()

base.execute('DROP TABLE IF EXISTS data')
base.commit()
base.close()
