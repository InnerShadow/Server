
class DataBaseCreater:
    def __init__(self, cur):
        self.cur = cur


    #Create tables if it is first init
    def initDataBase(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS roles (
                            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            role_name TEXT
                            )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            role_id INTEGER NOT NULL DEFAULT 1,
                            login TEXT,
                            password_hash TEXT,
                            password_salt TEXT,
                            ip_address TEXT,
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
                            FOREIGN KEY (user_id) REFERENCES users(user_id)
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS billboard(
                            billboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            billboards_group_id INTEGER,
                            x_pos FLOAT NOT NULL,
                            y_pos FLOAT NOT NULL,
                            UNIQUE(x_pos, y_pos),
                            FOREIGN KEY (billboards_group_id) REFERENCES billboards_group(billboards_group_id) 
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ad(
                            ad_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            video_url TEXT NOT NULL,
                            ad_name TEXT
                            )""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ad_schedule(
                            schedule_id INTEGER,
                            ad_id INTEGER,
                            priority INTEGER NOT NULL DEFAULT 1,
                            FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id),
                            FOREIGN KEY (ad_id) REFERENCES ad(ad_id)
                            )""")
        
