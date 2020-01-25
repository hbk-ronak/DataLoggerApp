import sqlite3

con = sqlite3.connect('user.db')

with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute('create table users (email TEXT, password TEXT)')
    cur.execute("insert into users values ('username', 'password') ;")
    # cur.commit()

con.close()
