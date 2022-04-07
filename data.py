import sqlite3
import time
from app import balance_usd, calculator


def create():
    conn = sqlite3.connect('nano.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE nano (name text,money float)""")
    c.execute("INSERT INTO nano VALUES ('my_eth',1.0)")
    c.execute("INSERT INTO nano VALUES ('month',1.2)")
    c.execute("INSERT INTO nano VALUES ('day',1.2)")
    conn.commit()
    conn.close()


def start():
    while True:
        try:
            start_time = time.time()
            conn = sqlite3.connect('nano.db')
            c = conn.cursor()
            cal = calculator()
            c.execute('''UPDATE nano SET money = ? WHERE name=?;''', (balance_usd(), "my_eth"))
            c.execute('''UPDATE nano SET money = ? WHERE name=?;''', (cal[4]['month'], "month"))
            c.execute('''UPDATE nano SET money = ? WHERE name=?;''', (cal[2]['day'], "day"))
            conn.commit()
            c.execute("SELECT * FROM nano")
            print(c.fetchall(), "%.3f" % (time.time() - start_time), "s")
        except:
            print("error")


if __name__ == '__main__':
    try:
        create()
        print("Log, table create")
    except:
        pass
    start()
