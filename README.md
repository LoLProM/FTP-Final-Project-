# FTP-Final-Project

Este proyecto es una implementación de un servidor y cliente FTP utilizando React para la interfaz de usuario y Python para el backend. El objetivo es proporcionar una solución simple y funcional para la transferencia de archivos a través del protocolo FTP, con un enfoque en la seguridad y la facilidad de uso.

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas:

- **client/**: Contiene la aplicación frontend construida con React.
  - **src/**: Archivos fuente de la aplicación React.
  - **public/**: Archivos estáticos como index.html.
  - **package.json**: Dependencias y scripts de npm.
  - **.env**: Variables de entorno para configuración (opcional).

- **server/**: Contiene el servidor FTP implementado en Python.
  - **app/**: Archivos fuente del servidor FTP.
  - **requirements.txt**: Dependencias del servidor.
  - **run_server.py**: Script para iniciar el servidor.

- **client_lib/**: Contiene la implementación del cliente FTP en Python.
  - **ftp_client.py**: Lógica del cliente FTP.
  - **security.py**: Capa de seguridad para el cliente.
  - **utils.py**: Funciones utilitarias para el cliente.

- **docs/**: Documentación del proyecto.

- **README.md**: Descripción general del proyecto.

## Requerimientos

### Para el servidor

Para ejecutar el servidor, necesitas tener instalado Python (versión 3.x) y las siguientes dependencias:

Puedes instalar las dependencias utilizando el siguiente comando:
bash:

`pip install -r server/requirements.txt`

### Para el cliente

Para ejecutar la aplicación frontend, necesitas tener instalado Node.js y npm. Luego, navega a la carpeta client/ y ejecuta los siguientes comandos:

1. Instalar las dependencias:

   `npm install`

2. Iniciar la aplicación:

   `npm start`

## Cómo Ejecutar el Proyecto

1. Primero, inicia el servidor desde la carpeta server/:

   `python run_server.py`

2. Luego, inicia la aplicación React desde la carpeta client/:

   `npm run dev`

3. Accede a la aplicación en tu navegador en <http://localhost:5173> (o el puerto que hayas configurado).
