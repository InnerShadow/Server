import os
import re
import socket

from DataBase.DataBase import *
from Entity.Timer import *
from Entity.Encoder import Encoder

class Server:
    def __init__(self, port : int):
        self.host = self.get_local_ip_address()
        self.port = port
        self.dataBase = DataBase()
        self.timer = Timer()
        self.encoder = Encoder()
        print(self.host)


    def get_local_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)
            
            s.connect(("8.8.8.8", 80))
            local_ip_address = s.getsockname()[0]
            s.close()
            
            return "127.0.0.9"
            return local_ip_address
        except Exception as e:
            print(f"Error getting local IP address: {e}")
            return None


    def start_server(self):

        #self.dataBase.register_user("127.0.0.5", "owner", "Dima", "1212")

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.host, self.port))
            server.listen(4)

            schedules_pattern = r'GET GROUP SCHEDULES schedules_name = (\w+)'
            ad_pattern = r'ad_path = (.*?)$'
            groop_owner_patter = r'GET GROOP BY OWNER owner = (\w+)'
            indendefication_pater = r'TRY TO LOG IN login = (\w+), password = (\w+)'
            register_patter = r'RESIGTER USER login = (\w+), password = (\w+), role = (\w+)'
            transfer_pattern = r'TRANSFER OWNERSHIP OF (\w+) TO (\w+)'
            create_schedules_pattern = r'CREATE SCHEDULES Schedule Name: (\w+)'
            edit_schedules_pattern = r"EDIT SCHEDULES schedules_name = "
            create_group_pattern = r'GET CREATE GROUP group_name = (\w+), schedule_name = (\w+)'

            while True:
                print('Working...')
                client_socket, client_address = server.accept()
                data = client_socket.recv(1024).decode('utf-8')

                schedules_match = re.search(schedules_pattern, data)
                ad_match = re.search(ad_pattern, data)
                groop_owner_match = re.search(groop_owner_patter, data)
                indendefication_match = re.search(indendefication_pater, data)
                register_match = re.search(register_patter, data)
                transfer_match = re.search(transfer_pattern, data)
                create_schedules_match = re.search(create_schedules_pattern, data)
                edit_schedules_match = re.search(edit_schedules_pattern, data)
                create_group_match = re.search(create_group_pattern, data)

                print(data)

                try:
                    if data == "GET_BILLBOARDS":
                        response_text = self.dataBase.Get_billboards()

                    elif data == "GET_TIME":
                        response_text = self.timer.init_time

                    elif data == "CONTINUE AS VIEWER":
                        self.dataBase.register_user(client_address[0], 'viewer', 'simple_viewer', 'password')
                        response_text = "OK"

                    elif data == "GET OWNERS":
                        response_text = self.dataBase.get_owners()

                    elif data == "GET ALL ADS":
                        response_text = self.dataBase.getAllAds()

                    elif data == "GET ALL SCHEDULES":
                        response_text = self.dataBase.getAllSchedules()

                    elif schedules_match:
                        schedules_name = schedules_match.group(1)
                        response_text = self.dataBase.Get_schedule_contents(schedules_name)

                    elif groop_owner_match:
                        owner = groop_owner_match.group(1)
                        response_text = self.dataBase.GetGroupsAndBillboardCounts(owner)

                    elif register_match:
                        username = register_match.group(1)
                        password = register_match.group(2)
                        role = register_match.group(3)
                        self.dataBase.register_user(client_address[0], role, username, password)

                    elif transfer_match:
                        billboard_grop = transfer_match.group(1)
                        username = transfer_match.group(2)
                        response_text = self.dataBase.transfer_ownership(username, billboard_grop)

                    elif create_group_match:
                        group_name = create_group_match.group(1)
                        schedule_name = create_group_match.group(2)
                        response_text = self.dataBase.createGroup(group_name, schedule_name)

                    elif create_schedules_match:
                        schedules_name = create_schedules_match.group(1)
                        ad_name_pattern = r'ad_name = (\w+(?: \w+)*)'
                        schedules = []

                        for match in re.finditer(ad_name_pattern, data):
                            schedules.append(match.group(1))

                        response_text = self.dataBase.create_schedule(schedules_name, schedules)

                    elif edit_schedules_match:
                        schedules_name = edit_schedules_match.group(1)
                        ad_name_pattern = r'ad_name = (\w+(?: \w+)*)'
                        schedules = []

                        for match in re.finditer(ad_name_pattern, data):
                            schedules.append(match.group(1))

                        response_text = self.dataBase.edit_schedule(schedules_name, schedules)


                    elif indendefication_match:
                        username = indendefication_match.group(1)
                        password = indendefication_match.group(2)

                        password_hash, salt = self.dataBase.getHashAndSalt(username)

                        if password_hash is None or salt is None:
                            response_text = "IDENTIFICATION NOT OK"

                        else:
                            role = self.dataBase.getRole(username)
                            resualt = self.encoder.checkpw(password, password_hash)
                            if resualt:
                                response_text = f"IDENDEFICATION OK role = {role} " 
                                self.dataBase.updateIP(username, client_address[0])

                            else:
                                response_text = "IDENDEFICATION NOT OK"

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
            self.dataBase.delete_viewers()
            server.close()
            print('Shutdown server.')

