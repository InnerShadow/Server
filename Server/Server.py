import socket

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def start_server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.host, self.port))
            server.listen(4)

            while True:
                print('Working...')
                client_socket, address = server.accept()
                data = client_socket.recv(1024).decode('utf-8')

                try:
                    number = int(data)
                    response = number * number
                    response_text = f"The square of {number} is {response}"
                except ValueError:
                    response_text = "Invalid input. Please send a valid number."

                headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
                context = response_text.encode('utf-8')

                client_socket.send(headers.encode('utf-8') + context)
                client_socket.shutdown(socket.SHUT_WR)
        except KeyboardInterrupt:
            server.close()
            print('Shutdown server.')

