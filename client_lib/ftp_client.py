import os
import re
import socket
from message import *
from .utils import get_file_size, read_file, write_file
from .security import generate_hash, verify_hash

TRUST_IN_PASS_IPV4 = False

class FTPClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bell_enable = False
        self.glob_enabled = True
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

    def allo(self, size):
        """
        Allocate given size in server to store files
        """

        response = self._send_command("ALLO " + str(size))

        if self.debug:
            print(f"Allocated {size} bytes in server")

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

    def hash(self, file_path):
        # Generar y verificar hash de un archivo
        file_hash = generate_hash(read_file(file_path))
        return file_hash

    def lcd(self, directory):
        # Cambiar el directorio de trabajo local
        os.chdir(directory)

    def bell(self, enable):
        # Activa o desactiva la campana
        self.bell_enabled = enable
        status = "activada" if enable else "desactivada"
        print(f"Campana {status}.")


    def site(self, params):
    # Enviar un comando SITE al servidor
        self._send_command(f'SITE {params}')
        self._get_response()

    def syst(self):
    # Obtener el tipo de sistema operativo del servidor
        self._send_command('SYST')
        return self._get_response()

    def help(self, command=None):
    # Obtener ayuda sobre comandos del servidor
        if command:
            self._send_command(f'HELP {command}')
        else:
            self._send_command('HELP')
        return self._get_response()

    def ls(self):
        # Mostrar el contenido del directorio en el servidor
        return self.dir()

    def stru(self, structure):
        """
        Set the file structure for file transfer.
        Structure codes:
        F - File (no record structure)
        R - Record structure
        P - Page structure
        """
        if structure not in ['F', 'R', 'P']:
            raise ValueError("Invalid structure. Use 'F', 'R', or 'P'.")
        self._send_command(f'STRU {structure}')
        self._get_response()


    def mode(self, mode):
            """
            Set the transfer mode.
            Modes:
            S - Stream (default)
            B - Block
            C - Compressed
            """
            if mode not in ['S', 'B', 'C']:
                raise ValueError("Invalid mode. Use 'S', 'B', or 'C'.")
            self._send_command(f'MODE {mode}')
            self._get_response()
    def prompt(self, command):
        # Confirmar comandos antes de ejecutarlos
        confirmation = input(f"¿Está seguro de que desea ejecutar el comando '{command}'? (s/n): ")
        if confirmation.lower() == 's':
            self._send_command(command)
            self._get_response()
        else:
            print("Comando cancelado.")

    def put(self, file_path):
        # Enviar un archivo al servidor
        file_size = get_file_size(file_path)
        file_name = os.path.basename(file_path)
        self._send_command(f'STOR {file_name}')
        self._get_response()
        with open(file_path, 'rb') as file:
            self.sock.sendfile(file)
        if self.bell_enabled:
            print('\a')  # Reproduce el sonido de la campana
        self._get_response()
        print(f"Archivo {file_path} subido exitosamente. Tamaño: {file_size} bytes.")

    def mput(self, file_paths):
        # Enviar múltiples archivos al servidor
        for file_path in file_paths:
            self.put(file_path)

    def stou(self, file_path):
        # Enviar un archivo al servidor con un nombre único
        file_name = os.path.basename(file_path)
        self._send_command('STOU')
        response = self._get_response()
        unique_name = response.split()[-1]  # Obtener el nombre único generado
        with open(file_path, 'rb') as file:
            self.sock.sendfile(file)
        if self.bell_enabled:
            print('\a')  # Reproduce el sonido de la campana
        self._get_response()
        print(f"Archivo {file_path} subido exitosamente como {unique_name}.")

    def append(self, filename, dest_path):
        # Continuar una descarga que se ha cortado previamente
            file_size = os.path.getsize(dest_path) if os.path.exists(dest_path) else 0
            self._send_command(f'APPE {filename}')
            self._get_response()
            with open(dest_path, 'ab') as file:
                while True:
                    data = self.sock.recv(4096)
                    if not data:
                        break
                    file.write(data)
            self._get_response()

    def toggle_glob(self, state: bool):
        """Activa/desactiva la expansión de comodines (ej. mput, mget)."""
        self.glob_enabled = state
        print(f"Glob: {'Activado' if state else 'Desactivado'}")

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

    def command_info(self, command):
        # Obtener información sobre un comando específico del servidor
        self._send_command(f'HELP {command}')
        return self._get_response()

    def binary(self):
        # Activar el modo de transferencia binario
        self._send_command('TYPE I')
        self._get_response()

    def ascii(self):
        # Activar el modo de transferencia en modo texto ASCII
        self._send_command('TYPE A')
        self._get_response()

    def validate_150(self, response):
        """150 Opening binary mode data connection for file transfer ({size} bytes)"""
        if response[:3] != "150":
            raise error_reply(response)
        regular_expression_150 = re.compile(
            r"150 .* \((\d+) bytes\)", re.IGNORECASE | re.ASCII
        )
        m = regular_expression_150.match(response)
        return int(m.group(1)) if m else None

    def validate_227(self, response):
        """227 Entering Passive Mode (192,168,1,2,197,143)"""
        if response[:3] != "227":
            raise error_reply(response)
        regular_expresion_227 = re.compile(
            r"(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)", re.ASCII
        )
        m = regular_expresion_227.search(response)
        if not m:
            raise error_not_expected()
        n = m.groups()
        host = ".".join(n[:4])
        port = (int(n[4]) << 8) + int(n[5])
        return host, port

    def validate_229(self, response, peer):
        """229 Entering Extended Passive Mode (|||6446|)"""
        if response[:3] != "229":
            raise error_reply(response)
        host = peer[0]
        port = int(response.split("|")[-2])  # (|||port|).
        return host, port

    def validate_257(self, response):
        """257 "/home/usuario/directorio" is the current directory"""
        if response[:3] != "257":
            raise error_reply(response)
        if response[3:5] != ' "':
            return ""
        directory_name = ""
        i = 5
        n = len(response)
        while i < n:
            c = response[i]
            i += 1
            if c == '"':
                if i >= n or response[i] != '"':
                    break
                i += 1
                directory_name += c
        return directory_name

    def sendport(self, host, port):  # 318 sendport and sendeprt
        if self.af == socket.AF_INET:
            host = host.replace(".", ",")
            port = f"{port >> 8},{port & 0xff}"
            response = self.send_command(f"PORT {host},{port}")
        else:
            fields = ["", repr(2), host, repr(port), ""]
            response = self.send_command("EPRT " + "|".join(fields))

    def makeport(self):
        # https://es.wikipedia.org/wiki/Protocolo_de_transferencia_de_archivos
        """Create a new socket and send a PORT command for the data channel."""
        sock = socket.create_server(("", 0), family=self.af, backlog=1)
        port = sock.getsockname()[1]
        host = self.sock.getsockname()[0]
        self.sendport(host, port)
        return sock

    def passive_connection(self, command, rest=None):
        host, port = self.make_passive_server()

        connection = socket.create_connection(
            (host, port), self.timeout, source_address=self.source_address
        )
        try:
            if rest is not None:
                self.send_command(f"REST {rest}")
            response = self.send_command(command)
            if response[0] == 2:
                response = self.get_response()
            if response[0] != "1":
                raise error_reply(response)
            return (connection, response)
        except:
            connection.close()
            raise

    def active_connection(self, command, rest=None):
        with self.makeport() as sock:
            if rest is not None:
                self.send_command(f"REST {rest}")
            response = self.send_command(command)
            if response[0] == 2:
                response = self.get_response()
            if response[0] != "1":
                raise error_reply(response)
            connection, _ = sock.accept()
            connection.timeout(self.timeout)
        return connection

    def create_subprocess(self, command, rest=None):
        """
        Create New Connection for the transfer data
        """

        if self.passive_server:
            return self.passive_connection(command, rest)
        else:
            with self.makeport() as sock:
                if rest is not None:
                    self.send_command(f"REST {rest}")
                response = self.send_command(command)
                if response[0] == "2":
                    response = self.get_response()
                if response[0] != "1":
                    raise error_reply(response)
                connection, _ = sock.accept()
                connection.timeout(self.timeout)
        if response[:3] == "150":
            size = self.validate_150(response)
        return connection, size

    def set_passive_server(self, val):
        self.passive_server = val

    def make_passive_server(self):
        if self.af == socket.AF_INET:
            parmas = self._send_command("PASV")
            host, port = self.validate_227(parmas)
            if not TRUST_IN_PASS_IPV4:
                host = self.sock.getpeername()[0]
        else:
            host, port = self.validate_229(
                self.send_command("EPSV"), self.sock.getpeername()
            )
        return host, port
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

    def quit(self):
        # Finalizar una conexión FTP sin cerrar el programa
        self._send_command('QUIT')
        self._get_response()

    def shell(self):
        # Salir a la línea de comandos temporalmente sin cortar la conexión
        os.system('/bin/bash')

    def abort(self):
            # Abortar el comando FTP previo y cualquier transferencia de datos asociada
            self._send_command('ABOR')
            response = self._get_response()
            if '226' in response:
                print("Comando abortado exitosamente. Transferencia de datos completada.")
            elif '426' in response:
                print("Comando abortado. Transferencia de datos terminada anormalmente.")
            else:
                print("Respuesta inesperada del servidor.")


    def command_loop(self):
        # Bucle para recibir comandos del usuario
        while True:
            command = input("ftp> ")
            if command == '!':
                self.shell()
            elif command.lower() == 'quit':
                self.quit()
                break
            else:
                self._send_command(command)
                self._get_response()


    def restart(self, marker):
            # Reiniciar la transferencia de archivos desde un punto específico
            self._send_command(f'REST {marker}')
            self._get_response()

    def user(self, username, password):
        # Cambiar el nombre de usuario y contraseña sin salir de la sesión FTP
        self._send_command(f'USER {username}')
        self._get_response()
        self._send_command(f'PASS {password}')
        self._get_response()
