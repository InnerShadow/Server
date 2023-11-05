from datetime import datetime

class Timer:
    def __init__(self):
        self.init_time = datetime.now().isoformat()
        pass


    def getCurrentTime(self):
        return datetime.now().isoformat()
    

    def get_log_time(self):
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time
    
