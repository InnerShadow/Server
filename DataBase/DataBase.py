import sqlite3 as sq

from Entity.Encoder import Encoder
from Entity.VideoPreprocer import VideoPreprocer
from DataBase.DataBaseCreater import DataBaseCreater

class DataBase:
    def __init__(self):
        with sq.connect("Data/billboards.db") as con:
            self.con = con
            self.cur = con.cursor()
            self.create_tables()
            self.create_roles()
            con.commit()

    
    def create_tables(self):
        DBcreater = DataBaseCreater(self.cur)
        DBcreater.initDataBase()


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


    def Get_schedule_contents(self, schedule_name : str):
        query = """
            SELECT A.video_url, A.ad_name
            FROM ad AS A
            JOIN ad_schedule AS ADSchedule ON A.ad_id = ADSchedule.ad_id
            JOIN schedule AS S ON ADSchedule.schedule_id = S.schedule_id
            WHERE S.schedule_name = ?
            ORDER BY ADSchedule.priority"""
        
        self.cur.execute(query, (schedule_name, ))
        result = self.cur.fetchall()

        videoPreprocer = VideoPreprocer()

        return " \n ".join([f"Video_url: {video_url}, Ad_name: {ad_name}, Ad_duration: {videoPreprocer.get_video_duration(video_url)}" for video_url, ad_name in result])
    

    def GetGroupsAndBillboardCounts(self, owner_name : str):
        query = """
            SELECT BG.group_name, COUNT(B.billboard_id) AS billboard_count
            FROM billboards_group AS BG
            JOIN ownership AS O ON BG.billboards_group_id = O.billboards_group_id
            JOIN users AS U ON O.user_id = U.user_id
            JOIN billboard AS B ON BG.billboards_group_id = B.billboards_group_id
            WHERE U.login = ?
            GROUP BY BG.group_name"""
        
        self.cur.execute(query, (owner_name, ))
        result = self.cur.fetchall()

        return " \n ".join([f"Group: {group_name}, Billboard_Count: {billboard_count}" for group_name, billboard_count in result])
    

    def getHashAndSalt(self, username: str):
        query = """
            SELECT U.password_hash, U.password_salt
            FROM users as U
            WHERE U.login = ?"""
        
        self.cur.execute(query, (username, ))
        result = self.cur.fetchone()

        if result is not None:
            return result[0], result[1]
        else:
            return None, None 


    def updateIP(self, username : str, ip_address : str):
        query = "UPDATE users SET ip_address = ? WHERE login = ?"
        self.cur.execute(query, (ip_address, username))
        self.con.commit()

    
    def register_user(self, ip_address : str, role : str = None, username : str = None, password : str = None):
        encoder = Encoder()

        if role == 'viewer':
            role_id = 1
        elif role == 'owner':
            role_id = 2
        elif role == 'admin':
            role_id = 3

        salt, hashed_password = encoder.getSaltAndHash(password)

        self.cur.execute("INSERT INTO users (role_id, login, password_hash, password_salt, ip_address) VALUES (?, ?, ?, ?, ?)"
                         , (role_id, username, hashed_password, salt, ip_address))
        
        self.con.commit()

    
    def getRole(self, username : str):
        query = """
            Select R.role_name
            FROM roles as R 
            INNER JOIN users as U ON U.role_id = R.role_id
            WHERE U.login = ?"""

        self.cur.execute(query, (username, ))
        result = self.cur.fetchone()

        return result[0]


    def delete_viewers(self):
        query = """
            DELETE FROM users
            WHERE login = 'simple_viewer' AND role_id = (
                SELECT role_id FROM roles WHERE role_name = 'viewer'
            )"""
        
        self.cur.execute(query)
        self.con.commit()


    def get_owners(self):
        query = """
            SELECT login
            FROM users
            WHERE role_id = (SELECT role_id FROM roles WHERE role_name = 'owner')"""

        self.cur.execute(query)
        result = self.cur.fetchall()
        owner_names = [row[0] for row in result]

        return " \n ".join([f"Owner name = {owner_name}" for owner_name in owner_names])


    def transfer_ownership(self, transfer_to : str, billboard_group_name : str):

        query = "SELECT user_id FROM users WHERE login = ?"
        self.cur.execute(query, (transfer_to, ))
        new_owner_id = self.cur.fetchone()

        query = "SELECT billboards_group_id FROM billboards_group WHERE group_name = ?"
        self.cur.execute(query, (billboard_group_name, ))
        group_id = self.cur.fetchone()

        query = "SELECT user_id FROM ownership WHERE billboards_group_id = ?"
        self.cur.execute(query, (group_id[0], ))
        current_owner_id = self.cur.fetchone()

        query = """
            UPDATE ownership
            SET user_id = ?
            WHERE billboards_group_id = ? AND user_id = ? """

        self.cur.execute(query, (new_owner_id[0], group_id[0], current_owner_id[0]))
        self.con.commit()

        return "Ownership transferred successfully"


    def getAllAds(self):
        query = "SELECT ad_name FROM ad"

        self.cur.execute(query)
        result = self.cur.fetchall()
        ads = [row[0] for row in result]

        return " \n ".join([f"Ad = {ad_name}" for ad_name in ads]) + " "


    def create_schedule(self, schedulesName, ad_list):
        query = "SELECT schedule_id FROM schedule WHERE schedule_name = ?"
        self.cur.execute(query, (schedulesName,))
        existing_schedule_id = self.cur.fetchone()

        if existing_schedule_id:
            return "Schedule with the same name already exists"

        query = "INSERT INTO schedule (schedule_name) VALUES (?)"
        self.cur.execute(query, (schedulesName,))
        self.con.commit()

        query = "SELECT schedule_id FROM schedule WHERE schedule_name = ?"
        self.cur.execute(query, (schedulesName,))
        schedule_id = self.cur.fetchone()

        if not schedule_id:
            return "Failed to create schedule"

        for priority, ad_name in enumerate(ad_list, start=1):
            query = """
                INSERT INTO ad_schedule (schedule_id, ad_id, priority)
                SELECT ?, A.ad_id, ?
                FROM ad AS A
                WHERE A.ad_name = ?
            """
            self.cur.execute(query, (schedule_id[0], priority, ad_name))
        
        self.con.commit()

        return "Schedule created successfully"
    
    