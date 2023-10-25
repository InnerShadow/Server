import socket
from DataBase.DataBase import *

class Server:

    def __init__(self, port):
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
            
            return local_ip_address
        except Exception as e:
            print(f"Error getting local IP address: {e}")
            return None


    def start_server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.host, self.port))
            server.listen(4)

            with open('Data/BillBoards.txt', 'r') as file:
                data = file.read()

            billboards = [line.split() for line in data.split('\n') if line.strip()]
            billboards = [(int(x), int(y)) for x, y in billboards]

            while True:
                print('Working...')
                client_socket, address = server.accept()
                data = client_socket.recv(1024).decode('utf-8')

                try:
                    if data == "GET_BILLBOARDS":
                        response_text = "\n".join([f"X: {x}, Y: {y}" for x, y in billboards])
                    else:
                        response_text = "Invalid input. Please send 'GET_BILLBOARDS'."

                    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
                    context = response_text.encode('utf-8')

                    client_socket.send(headers.encode('utf-8') + context)
                    client_socket.shutdown(socket.SHUT_WR)
                except Exception as e:
                    print(f"Error: {e}")
        except KeyboardInterrupt:
            server.close()
            print('Shutdown server.')

