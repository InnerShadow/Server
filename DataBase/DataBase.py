import sqlite3 as sq

class DataBase():

    def __init__(self):
        with sq.connect("Data/billbiards.db") as con:
            self.cur = con.cursor()

            self.cur.execute("""CREATE TABLE IN FO EXIST roles (
                             role_id INTEGER PRIMARY KEY AUTOINCRIMENT,
                             role_name TEXT
                             )""")

            self.cur.execute("""CREATE TABLE IN FO EXIST users (
                             user_id INTEGER PRIMARY KEY AUTOINCRIMENT,
                             login TEXT,
                             password_hash INTEGER,
                             FOREIGN KEY (role_id) REFERENCES roles(role_id) NOT NULL DEFAULT 1
                             )""")
            
            self.cur.execute("""CREATE TABLE IN FO EXIST schedual(
                             schedual_id INTEGER PRIMARY KEY AUTOINCRIMENT,
                             schedual_name TEXT 
                             )""")

    pass
