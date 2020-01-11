import random
import string
import sqlite3
import math

def id_generator():
    id_num=''
    length=8
    id_num += string.digits
    id_num += string.ascii_letters
    id_num += "@#*&_-"
    return ''.join(random.choice(id_num) for _ in range(length))


def insert_database():
    connection = sqlite3.connect('Simulation_data.db')
    cur = connection.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS dataset (
    useless_primary_key INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL,
    arrival REAL NOT NULL,
    duration INTEGER NOT NULL
    )""")
    i = 10000 - len(cur.fetchall())
    for _ in range(i):
        ID = id_generator()
        Arrival = random.uniform(1,10000)
        Duration = math.ceil(random.expovariate(1))
        cur.execute("INSERT INTO dataset(id, arrival, duration) VALUES(?,?,?)", (ID, Arrival, Duration))
    connection.commit()
    connection.close()

insert_database()
