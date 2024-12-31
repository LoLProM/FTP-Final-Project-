import os
import socket
from .utils import get_file_size, read_file, write_file
from .security import generate_hash, verify_hash

class FTPClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.sock.connect((self.host, self.port))
        self._get_response()
        self._send_command(f'USER {self.username}')
        self._get_response()
        self._send_command(f'PASS {self.password}')
        self._get_response()

    def _send_command(self, command):
        self.sock.sendall(f'{command}\r\n'.encode())

    def _get_response(self):
        response = self.sock.recv(4096).decode()
        print(response)
        return response

    def upload_file(self, file_path):
        file_size = get_file_size(file_path)
        file_name = os.path.basename(file_path)
        self._send_command(f'STOR {file_name}')
        self._get_response()
        with open(file_path, 'rb') as file:
            self.sock.sendfile(file)
        print(f"Archivo {file_path} subido exitosamente. Tamaño: {file_size} bytes.")

    def download_file(self, file_name, dest_path):
        self._send_command(f'RETR {file_name}')
        self._get_response()
        with open(dest_path, 'wb') as file:
            while True:
                data = self.sock.recv(4096)
                if not data:
                    break
                file.write(data)
        print(f"Archivo {file_name} descargado exitosamente a {dest_path}.")

    def list_files(self):
        self._send_command('LIST')
        response = self._get_response()
        print("Archivos en el servidor FTP:")
        print(response)

    def close(self):
        self._send_command('QUIT')
        self.sock.close()
        print("Conexión FTP cerrada.")
