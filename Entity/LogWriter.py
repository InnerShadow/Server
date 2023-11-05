import re

from DataBase.DataBase import DataBase
from Entity.Timer import Timer

class LogWriter:
    def __init__(self, dataBase : DataBase, timer : Timer):
        self.dataBase = dataBase
        self.timer = timer

        self.file = open("Data/logs.txt", 'a')


    def get_billboards(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get billboards \n")
        self.file.flush()


    def get_time(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get time \n")
        self.file.flush()

    
    def continue_as_viewer(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to continue as user \n")
        self.file.flush()

    
    def get_owners(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get owners \n")
        self.file.flush()


    def get_allAds(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to all ads \n")
        self.file.flush()

    
    def get_allSchedules(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get all schedules \n")
        self.file.flush()


    def get_all_users(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get all users \n")
        self.file.flush()

    
    def get_schedule_discription(self, ip_address : str, schedule : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get {schedule} schedule discription \n")
        self.file.flush()

    
    def get_group_discription(self, ip_address : str, owner : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get group discription from owner {owner} \n")
        self.file.flush()

    
    def get_resister(self, ip_address : str, user : str, role : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to resiter new user {user} as {role} \n")
        self.file.flush()

    
    def get_transer_ownership(self, ip_address : str, user : str, group : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to transfer ownership of {group} to {user} \n")
        self.file.flush()

    
    def get_cerate_group(self, ip_address : str, group : str, schedule : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to create new {group} grooup with {schedule} schedule \n")
        self.file.flush()

    
    def get_groups_for_user(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get group for {user} owner \n")
        self.file.flush()

    
    def get_schedules_for_user(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to get schedules for {user} owner \n")
        self.file.flush()

    
    def get_move_to_group(self, ip_address : str, x_pos : float, y_pos : float, move_to : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to move billboard({x_pos}, {y_pos}) to {move_to} group \n")
        self.file.flush()


    def get_set_schedue(self, ip_address : str, schedule : str, group : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to set {schedule} schedue to {group} group \n")
        self.file.flush()


    def get_create_billboard(self, ip_address : str, user : str, group : str, x_pos : float, y_pos : float):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to create bibloard({x_pos}, {y_pos}) in {group} group for {user} user \n")
        self.file.flush()


    def get_delete_billboard(self, ip_address : str, x_pos : float, y_pos : float):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to delete bibloard({x_pos}, {y_pos}) \n")
        self.file.flush()

    
    def get_delete_billboard(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to delete {user} user \n")
        self.file.flush()


    def get_change_password(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   {user} user ask to change password \n")
        self.file.flush()

    
    def get_succses_change_password(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   {user} user succsesfully change pasword \n")
        self.file.flush()


    def get_error_change_password(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   {user} user faild to change pasword \n")
        self.file.flush()


    def get_create_schedules(self, ip_address : str, schedule_name : str, schedule : list[str]):
        schedule_list = ""
        for i in range(len(schedule)):
            schedule_list += f"{i + 1}: {schedule[i]}; "

        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to create new {schedule_name} schedule with context [{schedule_list}] \n")
        self.file.flush()


    def get_log_in(self, ip_address : str, name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   {name} try to log in \n")
        self.file.flush()


    def get_log_in_succses(self, ip_address : str, name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   {name} succsesfully loged in \n")
        self.file.flush()

    
    def get_log_in_failed(self, ip_address : str, name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   {name} faild to loged in \n")
        self.file.flush()


    def get_download_ad(self, ip_address : str, file_name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to download {file_name} ad \n")
        self.file.flush()


    def get_upload_ad(self, ip_address : str, file_name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to upload {file_name} ad \n")
        self.file.flush()


    def get_upload_ad_succses(self, ip_address : str, file_name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   succsesfully upload {file_name} file \n")
        self.file.flush()


    def get_start_up_server(self):
        self.file.write(f"{self.timer.getCurrentTime()}   :::   START UP SERVER \n")
        self.file.flush()


    def get_shout_down_server(self):
        self.file.write(f"{self.timer.getCurrentTime()}   :::   SHOUT DOWN SERVER \n")
        self.file.flush()


    def get_logs(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.getCurrentTime()}   :::   [{ip_address} - {username}]   :::   ask to export logs with filter {user} \n")
        self.file.flush()


    def close(self):
        self.file.close()


    def find_logs_by_name(self, name):
        matching_logs = []
        pattern = re.compile(r"\[([\d\.]+ - " + re.escape(name) + r")\]")

        with open("Data/logs.txt", 'r') as f:
            for line in f:
                if pattern.search(line):
                    matching_logs.append(line.strip())
        
        return '\n'.join(matching_logs)
    
