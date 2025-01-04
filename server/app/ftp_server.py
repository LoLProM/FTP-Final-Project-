import socket
import threading
from .handlers import handle_user, handle_pass, handle_stor, handle_retr, handle_list, handle_quit

class FTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor FTP escuchando en {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Conexión aceptada de {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_socket.sendall(b'220 Welcome to the FTP server.\r\n')
        while True:
            command = client_socket.recv(4096).decode().strip()
            if not command:
                break
            print(f"Comando recibido: {command}")
            if command.startswith('USER'):
                handle_user(command, client_socket)
            elif command.startswith('PASS'):
                handle_pass(command, client_socket)
            elif command.startswith('STOR'):
                handle_stor(command, client_socket)
            elif command.startswith('RETR'):
                handle_retr(command, client_socket)
            elif command.startswith('LIST'):
                handle_list(command, client_socket)
            elif command.startswith('QUIT'):
                handle_quit(command, client_socket)
                break
            else:
                client_socket.sendall(b'502 Command not implemented.\r\n')
