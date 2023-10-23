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
                             role_id INTEGER NOT NULL DEFAULT 1,
                             login TEXT,
                             password_hash INTEGER,
                             FOREIGN KEY (role_id) REFERENCES roles(role_id)
                             )""")
            
            self.cur.execute("""CREATE TABLE IN FO EXIST schedual(
                             schedual_id INTEGER PRIMARY KEY AUTOINCRIMENT,
                             schedual_name TEXT 
                             )""")
            
            self.cur.execute("""CREATE TABLE IN FO EXIST billboards_groop(
                             billboards_groop_id INTEGER PRIMARY KEY AUTOINCRIMENT,
                             groop_name TEXT,
                             schedual_id INTEGER,
                             FOREIGN KEY (schedual_id) REFERENCES schedual(schedual_id)
                             )""")
            
            self.cur.execute("""CREATE TABLE IN FO EXIST billboard(
                             billboard_id INTEGER PRIMARY KEY AUTOINCRIMENT,
                             schedual_id INTEGER,
                             x_pos FLOAT NOT NULL,
                             y_pos FLOAT NOT NULL,
                             UNIQUE(x_pos, y_pos),
                             FOREIGN KEY (schedual_id) REFERENCES schedual(schedual_id) 
                             )""")
            
            self.cur.execute("""CREATE TABLE IN FO EXIST ad(
                             ad_id INTEGER PRIMARY KEY AUTOINCRIMENT,
                             vidio_url TEXT NOT NULL,
                             ad_name TEXT
                             )""")
            
            self.cur.execute("""CREATE TABLE IN FO EXIST ad_schedual(
                             schedual_id INTEGER,
                             ad_id INTEGER,
                             priority INTEGER NOT NULL,
                             PRIMARY KEY(schedual_id, ad_id)
                             FOREIGN KEY (schedual_id) REFERENCES schedual(schedual_id)
                             FOREIGN KEY (ad_id) REFERENCES ad(ad_id))""")

    pass
