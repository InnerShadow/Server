import sqlite3 as sq

class DataBase():

    def __init__(self):
        with sq.connect("Data/billboards.db") as con:
            self.cur = con.cursor()

            self.create_tables()
            
            self.create_roles()

            con.commit()

    
    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS roles (
                            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            role_name TEXT
                            )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            role_id INTEGER NOT NULL DEFAULT 1,
                            login TEXT,
                            password_hash INTEGER,
                            FOREIGN KEY (role_id) REFERENCES roles(role_id)
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS schedule(
                            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            schedule_name TEXT 
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS billboards_group(
                            billboards_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            group_name TEXT,
                            schedule_id INTEGER,
                            FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id)
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ownership(
                            billboards_group_id INTEGER,
                            user_id INTEGER,
                            PRIMARY KEY(billboards_group_id, user_id),
                            FOREIGN KEY (billboards_group_id) REFERENCES billboards_group(billboards_group_id),
                            FOREIGN KEY (user_id) REFERENCES user(user_id)
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS billboard(
                            billboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            schedule_id INTEGER,
                            x_pos FLOAT NOT NULL,
                            y_pos FLOAT NOT NULL,
                            UNIQUE(x_pos, y_pos),
                            FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id) 
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ad(
                            ad_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            video_url TEXT NOT NULL,
                            ad_name TEXT
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ad_schedule(
                            schedule_id INTEGER,
                            ad_id INTEGER,
                            priority INTEGER NOT NULL,
                            PRIMARY KEY(schedule_id, ad_id),
                            FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id),
                            FOREIGN KEY (ad_id) REFERENCES ad(ad_id)
                            )""")

        
    def create_roles(self):
            self.cur.execute("SELECT role_name FROM roles")
            existing_roles = [row[0] for row in self.cur.fetchall()]
            
            roles_to_insert = [
                ('viewer',),
                ('owner',),
                ('admin',),
            ]
            
            for role in roles_to_insert:
                if role[0] not in existing_roles:
                    self.cur.execute("INSERT INTO roles (role_name) VALUES (?)", role)

            pass

    pass
