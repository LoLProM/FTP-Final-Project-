from flask import Flask, request, jsonify
from client_lib.ftp_client import FTPClient

app = Flask(__name__)

# Configuración del cliente FTP
FTP_HOST = 'localhost'
FTP_PORT = 21
FTP_USER = 'testuser'
FTP_PASS = 'testpass'

ftp_client = FTPClient(FTP_HOST, FTP_PORT, FTP_USER, FTP_PASS)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = f"./{file.filename}"
    file.save(file_path)
    ftp_client.put(file_path)
    return jsonify({"message": "Archivo subido exitosamente."})

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    dest_path = f"./{filename}"
    ftp_client.get(filename, dest_path)
    return jsonify({"message": "Archivo descargado exitosamente."})

@app.route('/list', methods=['GET'])
def list_files():
    files = ftp_client.ls()
    return jsonify({"files": files})

@app.route('/delete', methods=['DELETE'])
def delete_file():
    filename = request.args.get('filename')
    ftp_client.delete(filename)
    return jsonify({"message": "Archivo eliminado exitosamente."})

@app.route('/rename', methods=['POST'])
def rename_file():
    old_name = request.json['old_name']
    new_name = request.json['new_name']
    ftp_client.rename(old_name, new_name)
    return jsonify({"message": "Archivo renombrado exitosamente."})

if __name__ == '__main__':
    app.run(debug=True)
