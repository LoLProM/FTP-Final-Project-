import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from client_lib.ftp_client import FTPClient
from client_lib.utils import write_file, read_file

class TestFTPClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = 'localhost'
        cls.port = 21
        cls.username = 'testuser'
        cls.password = 'testpass'
        cls.ftp_client = FTPClient(cls.host, cls.port, cls.username, cls.password)
        cls.test_file_name = 'test_file.txt'
        cls.test_file_content = b'This is a test file.'

        # Crear un archivo de prueba
        write_file(cls.test_file_name, cls.test_file_content)

    @classmethod
    def tearDownClass(cls):
        # Eliminar el archivo de prueba
        if os.path.exists(cls.test_file_name):
            os.remove(cls.test_file_name)
        cls.ftp_client.close()

    def test_upload_file(self):
        self.ftp_client.put(self.test_file_name)
        # Aquí se puede agregar lógica para verificar que el archivo se subió correctamente

    def test_download_file(self):
        download_path = 'downloaded_test_file.txt'
        self.ftp_client.get(self.test_file_name, download_path)
        downloaded_content = read_file(download_path)
        self.assertEqual(downloaded_content, self.test_file_content)
        # Eliminar el archivo descargado
        if os.path.exists(download_path):
            os.remove(download_path)

    def test_list_files(self):
        files = self.ftp_client.ls()
        self.assertIn(self.test_file_name, files)

    def test_invalid_login(self):
        with self.assertRaises(Exception):
            FTPClient(self.host, self.port, 'invalid_user', 'invalid_pass')

    def test_upload_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.ftp_client.put('nonexistent_file.txt')

    def test_download_nonexistent_file(self):
        with self.assertRaises(Exception):
            self.ftp_client.get('nonexistent_file.txt', 'downloaded_nonexistent_file.txt')

    def test_cd(self):
        self.ftp_client.mkdir('test_dir')
        self.ftp_client.cd('test_dir')
        current_dir = self.ftp_client.pwd()
        self.assertIn('test_dir', current_dir)
        self.ftp_client.cd('..')
        self.ftp_client.rmdir('test_dir')

    def test_delete_file(self):
        self.ftp_client.put(self.test_file_name)
        self.ftp_client.delete(self.test_file_name)
        files = self.ftp_client.ls()
        self.assertNotIn(self.test_file_name, files)

    def test_rename_file(self):
        new_name = 'renamed_test_file.txt'
        self.ftp_client.put(self.test_file_name)
        self.ftp_client.rename(self.test_file_name, new_name)
        files = self.ftp_client.ls()
        self.assertIn(new_name, files)
        self.ftp_client.delete(new_name)

if __name__ == '__main__':
    unittest.main()
