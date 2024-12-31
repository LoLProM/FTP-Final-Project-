import os

# Función para obtener el tamaño de un archivo
def get_file_size(file_path):
    # Verifica si el archivo existe
    if os.path.isfile(file_path):
        return os.path.getsize(file_path)
    else:
        raise FileNotFoundError(f"El archivo {file_path} no existe.")

# Función para leer un archivo en modo binario
def read_file(file_path):
    # Verifica si el archivo existe
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            return file.read()
    else:
        raise FileNotFoundError(f"El archivo {file_path} no existe.")

# Función para escribir datos en un archivo en modo binario
def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)
