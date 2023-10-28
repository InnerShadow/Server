import sqlite3 as sq

class DataBase:

    def __init__(self):
        with sq.connect("Data/billboards.db") as con:
            self.cur = con.cursor()

            self.create_tables()
            
            self.create_roles()

            con.commit()

        pass

    
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
                            ip_address TEXT UNIQUE,
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
        pass


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
    

    def Get_billboards(self):
        query = """
            SELECT BG.group_name, U.login, S.schedule_name, B.x_pos, B.y_pos
            FROM billboards_group AS BG
            JOIN ownership AS O ON BG.billboards_group_id = O.billboards_group_id
            JOIN users AS U ON O.user_id = U.user_id
            JOIN schedule AS S ON BG.schedule_id = S.schedule_id
            JOIN billboard AS B ON BG.billboards_group_id = B.billboards_group_id"""
        
        self.cur.execute(query)
        result = self.cur.fetchall()

        return " \n ".join([f"Group: {group_name}, Owner: {owner}, Schedule: {schedule_name}, X: {x}, Y: {y}" for group_name, owner, schedule_name, x, y in result])


    def Get_schedule_contents(self, schedule_name):
        query = """
            SELECT A.video_url, A.ad_name
            FROM ad AS A
            JOIN ad_schedule AS ADSchedule ON A.ad_id = ADSchedule.ad_id
            JOIN schedule AS S ON ADSchedule.schedule_id = S.schedule_id
            WHERE S.schedule_name = ?
            ORDER BY ADSchedule.priority"""
        
        self.cur.execute(query, (schedule_name,))
        result = self.cur.fetchall()

        print(result)

        return " \n ".join([f"Video_url: {video_url}, Ad_name: {ad_name}" for video_url, ad_name in result])

    pass

