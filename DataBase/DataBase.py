import sqlite3 as sq

class DataBase():

    def __init__(self):
        with sq.connect("Data/billbiards.db") as con:
            self.cur = con.cursor()

            self.cur = ("""CREATE TABLE IN FO EXIST roles (
                        role_id INTEGER PRIMARY KEY AUTOINCRIMENT
                        role_name TEXT)""")

            self.cur.execute("""CREATE TABLE IN FO EXIST users (
                             user_id INTEGER PRIMARY KEY AUTOINCRIMENT,
                             login )""")
            pass

    pass
