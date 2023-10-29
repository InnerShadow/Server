import os
import re
import socket

from DataBase.DataBase import *
from Entity.Timer import *

class Server:
    def __init__(self, port : int):
        self.host = self.get_local_ip_address()
        self.port = port
        self.dataBase = DataBase()
        self.timer = Timer()
        print(self.host)


    def get_local_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)
            
            s.connect(("8.8.8.8", 80))
            local_ip_address = s.getsockname()[0]
            s.close()
            
            return "127.0.0.7"
            return local_ip_address
        except Exception as e:
            print(f"Error getting local IP address: {e}")
            return None


    def start_server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.host, self.port))
            server.listen(4)

            schedules_pattern = r'GET GROUP SCHEDULES schedules_name = (\w+)'
            ad_pattern = r'ad_path = (.*?)$'
            groop_owner_patter = r'GET GROOP BY OWNER owner = (\w+)'

            while True:
                print('Working...')
                client_socket, address = server.accept()
                data = client_socket.recv(1024).decode('utf-8')

                schedules_match = re.search(schedules_pattern, data)
                ad_match = re.search(ad_pattern, data)
                groop_owner_match = re.search(groop_owner_patter, data)

                print(data)

                try:
                    if data == "GET_BILLBOARDS":
                        response_text = self.dataBase.Get_billboards()

                    elif data == "GET_TIME":
                        response_text = self.timer.init_time

                    elif schedules_match:
                        schedules_name = schedules_match.group(1)
                        response_text = self.dataBase.Get_schedule_contents(schedules_name)

                    elif groop_owner_match:
                        owner = groop_owner_match.group(1)
                        response_text = self.dataBase.GetGroupsAndBillboardCounts(owner)

                    elif ad_match:
                        vidio_url = ad_match.group(1)
                        response_text = open(vidio_url, 'rb').read()

                    else:
                        response_text = "Invalod request!"

                    if isinstance(response_text, str):
                        print(response_text)
                        context = response_text.encode('utf-8')

                    elif isinstance(response_text, bytes):
                        context = response_text

                    else:
                        context = b''  

                    client_socket.send(context)
                    client_socket.shutdown(socket.SHUT_WR)
                except Exception as e:
                    print(f"Error: {e}")
        except KeyboardInterrupt:
            server.close()
            print('Shutdown server.')

