from datetime import datetime

class Timer:
    def __init__(self):
        self.init_time = datetime.now().isoformat()
        pass


    def getCurrentTime(self):
        return datetime.now().isoformat()
    
