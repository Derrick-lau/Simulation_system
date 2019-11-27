import random
import string
import sqlite3

def id_generator():
    id_num=''
    length=6
    id_num += string.digits
    id_num += string.ascii_letters
    id_num += "@#*&_-"
    return ''.join(random.choice(id_num) for _ in range(length))


def insert_database():
    connection = sqlite3.connect('Simulation_data.db')
    cur = connection.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS dataset (
    id TEXT PRIMARY KEY UNIQUE NOT NULL,
    arrival REAL NOT NULL,
    duration INTEGER NOT NULL
    )""")
    print(len(cur.fetchall()))
    cur.execute("SELECT * FROM dataset ORDER BY arrival ASC")
    if len(cur.fetchall()) < 100:
        for _ in range(100):
            ID = id_generator()
            Arrival = random.uniform(1,100)
            Duration = round(random.expovariate(1))+1
            cur.execute("INSERT INTO dataset(id, arrival, duration) VALUES(?,?,?)", (ID, Arrival, Duration))
    cur.execute("SELECT * FROM dataset ORDER BY arrival ASC")
    print(cur.fetchall())
    connection.commit()
    connection.close()

insert_database()



   



 

