import os

def handle_user(command, client_socket):
    client_socket.sendall(b'331 Username OK, need password.\r\n')

def handle_pass(command, client_socket):
    client_socket.sendall(b'230 User logged in, proceed.\r\n')

def handle_stor(command, client_socket):
    filename = command.split()[1]
    client_socket.sendall(b'150 File status okay; about to open data connection.\r\n')
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            file.write(data)
    client_socket.sendall(b'226 Transfer complete.\r\n')

def handle_retr(command, client_socket):
    filename = command.split()[1]
    if os.path.isfile(filename):
        client_socket.sendall(b'150 File status okay; about to open data connection.\r\n')
        with open(filename, 'rb') as file:
            while True:
                data = file.read(4096)
                if not data:
                    break
                client_socket.sendall(data)
        client_socket.sendall(b'226 Transfer complete.\r\n')
    else:
        client_socket.sendall(b'550 File not found.\r\n')

def handle_list(command, client_socket):
    client_socket.sendall(b'150 Here comes the directory listing.\r\n')
    files = os.listdir('.')
    response = '\r\n'.join(files) + '\r\n'
    client_socket.sendall(response.encode())
    client_socket.sendall(b'226 List transfer done.\r\n')

def handle_quit(command, client_socket):
    client_socket.sendall(b'221 Goodbye.\r\n')
    client_socket.close()
