import re
from datetime import datetime

from DataBase.DataBase import DataBase
from Entity.Timer import Timer

#Write logs in "Data/logs.txt"
class LogWriter:
    def __init__(self, dataBase : DataBase, timer : Timer):
        self.dataBase = dataBase
        self.timer = timer

        self.total_ads = 0

        self.init_total_ads()

        self.file = open("Data/logs.txt", 'a')

    
    def init_total_ads(self):
        ads_pattern = r'ads showed befor shut down - (\w+) '

        try:
            with open("Data/logs.txt", 'r') as f:
                for line in f:
                    watch_match = re.search(ads_pattern, line)
                    if watch_match:
                        self.total_ads = int(watch_match.group(1))
        
        except Exception:
            self.total_ads = 0


    def get_billboards(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get billboards \n")
        self.file.flush()


    def get_time(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get time \n")
        self.file.flush()

    
    def continue_as_viewer(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to continue as user \n")
        self.file.flush()

    
    def get_owners(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get owners \n")
        self.file.flush()


    def get_allAds(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to all ads \n")
        self.file.flush()

    
    def get_allSchedules(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get all schedules \n")
        self.file.flush()


    def get_all_users(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get all users \n")
        self.file.flush()

    
    def get_schedule_discription(self, ip_address : str, schedule : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get {schedule} schedule discription \n")
        self.file.flush()

    
    def get_group_discription(self, ip_address : str, owner : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get group discription from owner {owner} \n")
        self.file.flush()

    
    def get_resister(self, ip_address : str, user : str, role : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to resiter new user {user} as {role} \n")
        self.file.flush()

    
    def get_transer_ownership(self, ip_address : str, user : str, group : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to transfer ownership of {group} to {user} \n")
        self.file.flush()

    
    def get_cerate_group(self, ip_address : str, group : str, schedule : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to create new {group} grooup with {schedule} schedule \n")
        self.file.flush()

    
    def get_groups_for_user(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get group for {user} owner \n")
        self.file.flush()

    
    def get_schedules_for_user(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to get schedules for {user} owner \n")
        self.file.flush()

    
    def get_move_to_group(self, ip_address : str, x_pos : float, y_pos : float, move_to : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to move billboard({x_pos}, {y_pos}) to {move_to} group \n")
        self.file.flush()


    def get_set_schedue(self, ip_address : str, schedule : str, group : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to set {schedule} schedue to {group} group \n")
        self.file.flush()


    def get_create_billboard(self, ip_address : str, user : str, group : str, x_pos : float, y_pos : float):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to create bibloard({x_pos}, {y_pos}) in {group} group for {user} user \n")
        self.file.flush()


    def get_delete_billboard(self, ip_address : str, x_pos : float, y_pos : float):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to delete bibloard({x_pos}, {y_pos}) \n")
        self.file.flush()

    
    def get_delete_user(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to delete {user} user \n")
        self.file.flush()


    def get_change_password(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   {user} user ask to change password \n")
        self.file.flush()

    
    def get_succses_change_password(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   {user} user succsesfully change pasword \n")
        self.file.flush()


    def get_error_change_password(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   {user} user faild to change pasword \n")
        self.file.flush()


    def get_create_schedules(self, ip_address : str, schedule_name : str, schedule : list[str]):
        schedule_list = ""
        for i in range(len(schedule)):
            schedule_list += f"{i + 1}: {schedule[i]}; "

        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to create new {schedule_name} schedule with context [{schedule_list}] \n")
        self.file.flush()


    def get_log_in(self, ip_address : str, name : str):
        username = self.dataBase.userForIP(ip_address)
        if username is None:
            self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - Undefined]   :::   {name} try to log in \n")
        else:
            self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   {name} try to log in \n")
        self.file.flush()


    def get_log_in_succses(self, ip_address : str, name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   {name} succsesfully loged in \n")
        self.file.flush()

    
    def get_log_in_failed(self, ip_address : str, name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   {name} faild to loged in \n")
        self.file.flush()


    def get_download_ad(self, ip_address : str, file_name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to download {file_name} ad \n")
        self.file.flush()


    def get_upload_ad(self, ip_address : str, file_name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to upload {file_name} ad \n")
        self.file.flush()


    def get_upload_ad_succses(self, ip_address : str, file_name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   succsesfully upload {file_name} file \n")
        self.file.flush()

    
    def get_exit_app(self, ip_address : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   exit application \n")
        self.file.flush()

    
    def get_watch_ad(self, ip_address : str, ad_name : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   watch {ad_name} ad \n")
        self.file.flush()


    def get_start_up_server(self):
        self.file.write(f"{self.timer.get_log_time()}   :::   START UP SERVER \n")
        self.file.flush()


    def get_shout_down_server(self):
        self.file.write(f"{self.timer.get_log_time()}   :::   SHOUT DOWN SERVER \n")
        self.file.flush()


    def get_logs(self, ip_address : str, user : str):
        username = self.dataBase.userForIP(ip_address)
        self.file.write(f"{self.timer.get_log_time()}   :::   [{ip_address} - {username}]   :::   ask to export logs with filter {user} \n")
        self.file.flush()

    
    def get_ads_watched(self, ip_address : str):
        watched_ads_count = 0
        watch_pattern = r'watch (\w+) ad'

        with open("Data/logs.txt", 'r') as f:
            for line in f:
                watch_match = re.search(watch_pattern, line)
                if watch_match:
                    watched_ads_count += 1

        return str(watched_ads_count)

    
    def get_showed_ads(self, ip_address : str):
        durations : list[int] = []
        counts : list[int] = []

        schedules_pattern = r'Schedule: (\w+)'
        ads_pattern = r'Ad_duration: (\w+)'

        schedules_matches = re.findall(schedules_pattern, self.dataBase.Get_billboards())

        for schedule in schedules_matches:
            durations.append(0)
            counts.append(0)
            ads_matches = re.findall(ads_pattern, self.dataBase.Get_schedule_contents(schedule))
            for duration in ads_matches:
                durations[-1] += int(duration)
                counts[-1] += 1

        time_difference = datetime.now() - datetime.fromisoformat(self.timer.init_time)
        seconds_passed = int(time_difference.total_seconds())

        current_ads = self.total_ads

        for i in range(len(durations)):
            numOfCycles = seconds_passed // durations[i]
            numOfAds = numOfCycles * counts[i]
            current_ads += numOfAds
            #total_ads += (durations[i] // (seconds_passed % durations[i] + 1)) % counts[i]

        return str(current_ads)


    def save_ads_showed(self):
        current_ads = self.get_showed_ads("127.0.0.1")
        self.file.write(f"{self.timer.get_log_time()}   :::   ads showed befor shut down - {current_ads} \n")
        self.file.flush()


    def close(self):
        self.save_ads_showed()
        self.file.close()


    def find_logs_by_name(self, name):
        matching_logs = []
        pattern = re.compile(r"\[([\d\.]+ - " + re.escape(name) + r")\]")

        with open("Data/logs.txt", 'r') as f:
            lines = f.readlines()

        for line in lines:
            if pattern.search(line):
                matching_logs.append(line.strip())

        return '\n'.join(reversed(matching_logs))
    
