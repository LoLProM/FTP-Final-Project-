# Proyecto FTP Integrado

Este proyecto integra un servidor FTP, un cliente FTP, una API y una interfaz visual utilizando React. A continuación se explica cómo ejecutar todo el proyecto, cómo es la interacción entre los componentes, cómo están relacionados y cuál es la función de cada uno.

## Estructura del Proyecto

- `server`: Contiene el servidor FTP.
- `client_lib`: Contiene el cliente FTP.
- `api`: Contiene la API para conectar el frontend con el servidor FTP.
- `client`: Contiene la interfaz visual  React.

## Requisitos

- Python 3.x
- Node.js
- npm (Node Package Manager)

## Instrucciones para Ejecutar el Proyecto

### 1. Ejecutar el Servidor FTP

1. Navega al directorio `server`.
2. Ejecuta el siguiente comando:

   ```bash
   python run_server.py

### 2. Ejecutar la API

- Navega al directorio api.
- Instala las dependencias:

`pip install -r requirements.txt`

- Ejecuta la API:

`python app.py`

### 3. Ejecutar la Interfaz Visual

- Navega al directorio client_app.
- Instala las dependencias:

`npm install`

- Ejecuta la aplicación:

`npm start`

### Interacción entre los Componentes

#### Servidor FTP

El servidor FTP se encuentra en la carpeta server y se encarga de manejar las conexiones FTP, recibir comandos y realizar operaciones como subir, descargar, listar y eliminar archivos.

#### Cliente FTP

El cliente FTP se encuentra en la carpeta client_lib y se encarga de enviar comandos al servidor FTP y manejar las respuestas. Este cliente es utilizado por la API para realizar las operaciones necesarias.

#### API

La API se encuentra en la carpeta api y actúa como intermediario entre el frontend y el servidor FTP. Proporciona endpoints para subir, descargar, listar, eliminar y renombrar archivos. Utiliza el cliente FTP para comunicarse con el servidor FTP.

#### Interfaz Visual

La interfaz visual se encuentra en la carpeta client y está construida utilizando React. Permite a los usuarios interactuar con el servidor FTP de manera intuitiva a través de una interfaz moderna. La interfaz visual se comunica con la API para realizar las operaciones necesarias.

### Función de Cada Componente

- Servidor FTP: Maneja las conexiones FTP y realiza operaciones en los archivos.
- Cliente FTP: Envía comandos al servidor FTP y maneja las respuestas.
- API: Actúa como intermediario entre el frontend y el servidor FTP.
- Interfaz Visual: Permite a los usuarios interactuar con el servidor FTP de manera intuitiva.
Con estos pasos, deberías poder ejecutar todo el proyecto integrado y entender cómo interactúan los diferentes componentes.
