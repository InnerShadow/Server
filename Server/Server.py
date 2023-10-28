import socket
import re
from DataBase.DataBase import *


class Server:

    def __init__(self, port : int):
        self.host = self.get_local_ip_address()
        self.port = port
        self.dataBase = DataBase()
        print(self.host)


    def get_local_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)
            
            s.connect(("8.8.8.8", 80))
            local_ip_address = s.getsockname()[0]
            s.close()
            
            return "127.0.0.2"
            return local_ip_address
        except Exception as e:
            print(f"Error getting local IP address: {e}")
            return None


    def start_server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.host, self.port))
            server.listen(4)

            while True:
                print('Working...')
                client_socket, address = server.accept()
                data = client_socket.recv(1024).decode('utf-8')

                schedules_pattern = r'GET GROUP SCHEDULES schedules_name = (\w+)'
                schedules_match = re.search(schedules_pattern, data)

                try:
                    if data == "GET_BILLBOARDS":
                        response_text = self.dataBase.Get_billboards()
                            
                    if schedules_match:
                        schedules_name = schedules_match.group(1)
                        response_text = self.dataBase.Get_schedule_contents(schedules_name)

                    context = response_text.encode('utf-8')

                    client_socket.send(context)
                    client_socket.shutdown(socket.SHUT_WR)
                except Exception as e:
                    print(f"Error: {e}")
        except KeyboardInterrupt:
            server.close()
            print('Shutdown server.')
