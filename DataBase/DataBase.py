import sqlite3 as sq

from Entity.Encoder import Encoder
from Entity.VideoPreprocer import VideoPreprocer
from DataBase.DataBaseCreater import DataBaseCreater

#Class for execiting all nedeed SQL queryes
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

        return f"User {username} was created!"

    
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
                SELECT role_id FROM roles WHERE role_name = 'viewer')"""
        
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

    
    def getAllUsers(self):
        query = "SELECT login FROM users"

        self.cur.execute(query)
        result = self.cur.fetchall()
        users_names = [row[0] for row in result]

        return " \n ".join([f"User name = {user_name}" for user_name in users_names])


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


    def create_schedule(self, schedulesName : str, ad_list : list[str]):
        query = "SELECT schedule_id FROM schedule WHERE schedule_name = ?"
        self.cur.execute(query, (schedulesName,))
        existing_schedule_id = self.cur.fetchone()

        if existing_schedule_id:
            return "Schedule with the same name already exists"

        query = "INSERT INTO schedule (schedule_name) VALUES (?)"
        self.cur.execute(query, (schedulesName,))
        self.con.commit()

        query = "SELECT schedule_id FROM schedule WHERE schedule_name = ?"
        self.cur.execute(query, (schedulesName, ))
        schedule_id = self.cur.fetchone()

        if not schedule_id:
            return "Failed to create schedule"

        for priority, ad_name in enumerate(ad_list, start=1):
            query = """
                INSERT INTO ad_schedule (schedule_id, ad_id, priority)
                SELECT ?, A.ad_id, ?
                FROM ad AS A
                WHERE A.ad_name = ?"""
            
            self.cur.execute(query, (schedule_id[0], priority, ad_name))
        
        self.con.commit()

        return "Schedule created successfully"
    

    def create_ad(self, file_name: str, file_path: str):
        query = "INSERT INTO ad (video_url, ad_name) VALUES (?, ?)"
        
        self.cur.execute(query, (file_path, file_name))
        
        self.con.commit()


    def edit_schedule(self, schedulesName: str, ad_list: list[str]):
        query = "SELECT schedule_id FROM schedule WHERE schedule_name = ?"
        self.cur.execute(query, (schedulesName, ))
        schedule_id = self.cur.fetchone()

        if not schedule_id:
            return "Schedule not found"

        query = "DELETE FROM ad_schedule WHERE schedule_id = ?"
        self.cur.execute(query, (schedule_id[0], ))

        for priority, ad_name in enumerate(ad_list, start = 1):
            query = """
                INSERT INTO ad_schedule (schedule_id, ad_id, priority)
                SELECT ?, A.ad_id, ?
                FROM ad AS A
                WHERE A.ad_name = ?"""
            
            self.cur.execute(query, (schedule_id[0], priority, ad_name))

        self.con.commit()

        return "Schedule updated successfully"


    def getAllSchedules(self):
        query = "SELECT schedule_name FROM schedule"

        self.cur.execute(query)
        result = self.cur.fetchall()
        schedules = [row[0] for row in result]

        return " \n ".join([f"Schedule Name = {schedule_name}" for schedule_name in schedules]) + " "


    def createGroup(self, group_name: str, schedule_name: str):
        query = "SELECT schedule_id FROM schedule WHERE schedule_name = ?"
        self.cur.execute(query, (schedule_name, ))
        existing_schedule_id = self.cur.fetchone()

        if not existing_schedule_id:
            return "Schedule not found"

        query = "INSERT INTO billboards_group (group_name, schedule_id) VALUES (?, ?)"
        self.cur.execute(query, (group_name, existing_schedule_id[0]))
        self.con.commit()

        return "Group created successfully"


    def getGroopsForUser(self, owner: str):
        query = """
            SELECT BG.group_name
            FROM billboards_group AS BG
            JOIN ownership AS O ON BG.billboards_group_id = O.billboards_group_id
            JOIN users AS U ON O.user_id = U.user_id
            WHERE U.login = ?
            UNION
            SELECT BG.group_name
            FROM billboards_group AS BG
            WHERE BG.billboards_group_id NOT IN (
                SELECT billboards_group_id
                FROM ownership)"""

        self.cur.execute(query, (owner, ))
        result = self.cur.fetchall()
        groups = [row[0] for row in result]

        return " \n ".join([f"Group Name = {group_name}" for group_name in groups]) + " "


    def moveBillboard(self, x_pos: float, y_pos: float, move_to: str):
        query = "SELECT billboards_group_id FROM billboards_group WHERE group_name = ?"
        self.cur.execute(query, (move_to,))
        group_id = self.cur.fetchone()

        if not group_id:
            return "Group not found"

        query = """
            SELECT O.user_id
            FROM ownership AS O
            JOIN billboard AS B ON O.billboards_group_id = B.billboards_group_id
            WHERE B.x_pos = ? AND B.y_pos = ?"""
        
        self.cur.execute(query, (x_pos, y_pos))
        user_id = self.cur.fetchone()

        if not user_id:
            return "Billboard not found"

        query = """
            INSERT OR REPLACE INTO ownership (billboards_group_id, user_id)
            VALUES (?, ?) """
        
        self.cur.execute(query, (group_id[0], user_id[0]))
        self.con.commit()

        query = """
            UPDATE billboard
            SET billboards_group_id = ?
            WHERE x_pos = ? AND y_pos = ?"""
        
        self.cur.execute(query, (group_id[0], x_pos, y_pos))
        self.con.commit()

        return "Billboard moved successfully"


    def getSchedulesForUser(self, owner: str):
        query = """
            SELECT DISTINCT S.schedule_name
            FROM schedule AS S
            LEFT JOIN ad_schedule AS ASch ON S.schedule_id = ASch.schedule_id
            LEFT JOIN ad AS A ON ASch.ad_id = A.ad_id
            LEFT JOIN billboards_group AS BG ON BG.schedule_id = S.schedule_id
            LEFT JOIN ownership AS O ON BG.billboards_group_id = O.billboards_group_id
            LEFT JOIN users AS U ON O.user_id = U.user_id
            WHERE U.login = ? OR BG.billboards_group_id IS NULL
            UNION
            SELECT DISTINCT S.schedule_name
            FROM schedule AS S
            WHERE S.schedule_id NOT IN (
                SELECT DISTINCT schedule_id
                FROM ad_schedule)"""

        self.cur.execute(query, (owner,))
        result = self.cur.fetchall()
        schedules = [row[0] for row in result]

        return " \n ".join([f"Schedule Name = {schedule_name}" for schedule_name in schedules]) + " "


    def setSchedules(self, schedules: str, group: str):
        query_schedule_id = "SELECT schedule_id FROM schedule WHERE schedule_name = ?"
        self.cur.execute(query_schedule_id, (schedules, ))
        schedule_id = self.cur.fetchone()

        if not schedule_id:
            return "Schedule not found"

        query_group_id = "SELECT billboards_group_id FROM billboards_group WHERE group_name = ?"
        self.cur.execute(query_group_id, (group, ))
        group_id = self.cur.fetchone()

        if not group_id:
            return "Group not found"

        query_update_group = "UPDATE billboards_group SET schedule_id = ? WHERE billboards_group_id = ?"
        self.cur.execute(query_update_group, (schedule_id[0], group_id[0]))
        self.con.commit()

        return "Schedules set successfully"


    def updatePassword(self, username: str, new_password : str):
        encoder = Encoder()
        salt, password_hash = encoder.getSaltAndHash(new_password)

        query_update_password = "UPDATE users SET password_salt = ?, password_hash = ? WHERE login = ?"
        self.cur.execute(query_update_password, (salt, password_hash, username))
        self.con.commit()

        return "Password updated successfully"

    
    def createBillboard(self, username: str, group: str, x_pos: float, y_pos: float):
        query = "SELECT user_id FROM users WHERE login = ?"
        self.cur.execute(query, (username, ))
        user_id = self.cur.fetchone()

        if not user_id:
            return "User not found"

        query = "SELECT billboards_group_id, schedule_id FROM billboards_group WHERE group_name = ?"
        self.cur.execute(query, (group, ))
        group_info = self.cur.fetchone()

        if not group_info:
            return "Billboards group not found"

        if not group_info[1]:
            schedule_name = f"{group} Schedule"
            query = "INSERT INTO schedule (schedule_name) VALUES (?)"
            self.cur.execute(query, (schedule_name, ))
            self.con.commit()

            query = "SELECT schedule_id FROM schedule WHERE schedule_name = ?"
            self.cur.execute(query, (schedule_name, ))
            schedule_id = self.cur.fetchone()
            if not schedule_id:
                return "Failed to create schedule"

            query = "UPDATE billboards_group SET schedule_id = ? WHERE billboards_group_id = ?"
            self.cur.execute(query, (schedule_id[0], group_info[0]))
            self.con.commit()

        query = "SELECT * FROM ownership WHERE billboards_group_id = ? AND user_id = ?"
        self.cur.execute(query, (group_info[0], user_id[0]))
        existing_ownership = self.cur.fetchone()

        query = "INSERT INTO billboard (billboards_group_id, x_pos, y_pos) VALUES (?, ?, ?)"
        self.cur.execute(query, (group_info[0], x_pos, y_pos))
        self.con.commit()

        if existing_ownership:
            return "Ownership relationship already exists"

        query = "INSERT INTO ownership (billboards_group_id, user_id) VALUES (?, ?)"
        self.cur.execute(query, (group_info[0], user_id[0]))
        self.con.commit()

        return "Billboard created successfully"


    def deleteBillboard(self, x_pos : float, y_pos : float):
        self.cur.execute("SELECT billboard_id FROM billboard WHERE x_pos = ? AND y_pos = ?", (x_pos, y_pos))
        result = self.cur.fetchone()

        billboard_id = result[0]
        self.cur.execute("DELETE FROM billboard WHERE billboard_id = ?", (billboard_id,))

        self.con.commit()

        return "Billboard has been deleted"


    def deleteUser(self, username : str):
        query = "DELETE FROM users WHERE login = ?"

        self.cur.execute(query, (username, ))
        self.con.commit()

        return f"User {username} has been delted"
    

    def userForIP(self, ip_address : str):
        query = "SELECT login FROM users WHERE ip_address = ?"

        self.cur.execute(query, (ip_address, ))
        result = self.cur.fetchone()

        if result is not None:
            return result[0]
        
        else:
            return None
    
