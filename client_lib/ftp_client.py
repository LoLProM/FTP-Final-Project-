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
        # Conectar al servidor FTP
        self.sock.connect((self.host, self.port))
        self._get_response()
        self._send_command(f'USER {self.username}')
        self._get_response()
        self._send_command(f'PASS {self.password}')
        self._get_response()

    def _send_command(self, command):
        # Enviar comando al servidor FTP
        self.sock.sendall(f'{command}\r\n'.encode())

    def _get_response(self):
        # Obtener respuesta del servidor FTP
        response = self.sock.recv(4096).decode()
        print(response)
        return response

    def open(self, host, port):
        # Iniciar una conexión con un servidor FTP
        self.sock.connect((host, port))
        self._get_response()

    def close(self):
        # Finalizar una conexión FTP
        self._send_command('QUIT')
        self.sock.close()
        print("Conexión FTP cerrada.")

    def cd(self, directory):
        # Cambiar el directorio de trabajo en el servidor
        self._send_command(f'CWD {directory}')
        self._get_response()

    def delete(self, filename):
        # Borrar un archivo en el servidor
        self._send_command(f'DELE {filename}')
        self._get_response()

    def mdelete(self, pattern):
        # Borrar múltiples archivos basado en un patrón
        files = self.list_files()
        for file in files:
            if pattern in file:
                self.delete(file)

    def dir(self):
        # Mostrar el contenido del directorio en el servidor
        self._send_command('LIST')
        return self._get_response()

    def get(self, filename, dest_path):
        # Obtener un archivo del servidor
        self._send_command(f'RETR {filename}')
        self._get_response()
        with open(dest_path, 'wb') as file:
            while True:
                data = self.sock.recv(4096)
                if not data:
                    break
                file.write(data)
        self._get_response()

    def noop(self):
        # No Operation
        self._send_command('NOOP')
        self._get_response()

    def mget(self, filenames, dest_dir):
        # Obtener múltiples archivos del servidor
        for filename in filenames:
            self.get(filename, os.path.join(dest_dir, filename))

    def hash(self):
        # Implementación de barra de progreso con hashes
        pass

    def lcd(self, directory):
        # Cambiar el directorio de trabajo local
        os.chdir(directory)

    def ls(self):
        # Mostrar el contenido del directorio en el servidor
        return self.dir()

    def prompt(self):
        # Implementación de confirmación de comandos
        pass

    def put(self, file_path):
        # Enviar un archivo al servidor
        file_size = get_file_size(file_path)
        file_name = os.path.basename(file_path)
        self._send_command(f'STOR {file_name}')
        self._get_response()
        with open(file_path, 'rb') as file:
            self.sock.sendfile(file)
        self._get_response()
        print(f"Archivo {file_path} subido exitosamente. Tamaño: {file_size} bytes.")

    def mput(self, file_paths):
        # Enviar múltiples archivos al servidor
        for file_path in file_paths:
            self.put(file_path)

    def pwd(self):
        # Mostrar el directorio activo en el servidor
        self._send_command('PWD')
        return self._get_response()

    def rename(self, old_name, new_name):
        # Cambiar el nombre a un archivo en el servidor
        self._send_command(f'RNFR {old_name}')
        self._get_response()
        self._send_command(f'RNTO {new_name}')
        self._get_response()

    def rmdir(self, directory):
        # Eliminar un directorio en el servidor
        self._send_command(f'RMD {directory}')
        self._get_response()

    def status(self):
        # Mostrar el estado actual de la conexión
        self._send_command('STAT')
        return self._get_response()

    def binary(self):
        # Activar el modo de transferencia binario
        self._send_command('TYPE I')
        self._get_response()

    def ascii(self):
        # Activar el modo de transferencia en modo texto ASCII
        self._send_command('TYPE A')
        self._get_response()

    def literal(self, command):
        # Ejecutar comandos del servidor de forma remota
        self._send_command(command)
        self._get_response()

    def mkdir(self, directory):
        # Crear un directorio en el servidor
        self._send_command(f'MKD {directory}')
        self._get_response()

    def quote(self, command):
        # Ejecutar comandos del servidor de forma remota
        self.literal(command)

    def send(self, file_path):
        # Enviar un archivo al servidor
        self.put(file_path)

    def user(self, username, password):
        # Cambiar el nombre de usuario y contraseña sin salir de la sesión FTP
        self._send_command(f'USER {username}')
        self._get_response()
        self._send_command(f'PASS {password}')
        self._get_response()
