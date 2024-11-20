import os
import xml.etree.ElementTree as ET
import datetime
import unittest
import os
import tarfile
import datetime


class VirtualFileSystem:
    def __init__(self, vfs_path):
        self.vfs_path = vfs_path
        self.current_dir = vfs_path

    def ls(self):
        return os.listdir(self.current_dir)

    def cd(self, path):
        new_path = os.path.join(self.current_dir, path)
        if os.path.isdir(new_path):
            self.current_dir = new_path
            return f"Changed directory to {self.current_dir}"
        else:
            return "No such directory"

    def chmod(self, mode, filename):
        # Эмуляция изменения прав
        return f"Changed mode of {filename} to {mode}"

    def date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def tail(self, filename, lines=10):
        try:
            with open(os.path.join(self.current_dir, filename), 'r') as file:
                return ''.join(file.readlines()[-lines:])
        except FileNotFoundError:
            return "File not found"

class ShellEmulator:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.vfs = VirtualFileSystem(self.vfs_path)

    def load_config(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()
        self.computer_name = root.find('computer_name').text
        self.vfs_path = root.find('vfs_path').text

    def run(self):
        while True:
            command = input(f"{self.computer_name}@shell:{self.vfs.current_dir} $ ")
            if command.startswith("ls"):
                print(self.vfs.ls())
            elif command.startswith("cd"):
                _, path = command.split(maxsplit=1)
                print(self.vfs.cd(path))
            elif command.startswith("chmod"):
                _, mode, filename = command.split(maxsplit=2)
                print(self.vfs.chmod(mode, filename))
            elif command == "date":
                print(self.vfs.date())
            elif command.startswith("tail"):
                _, filename = command.split(maxsplit=1)
                print(self.vfs.tail(filename))
            elif command == "exit":
                break
            else:
                print("Unknown command")

class TestEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создание тестового tar-файла и конфигурации
        cls.test_tar = 'test_fs.tar'
        cls.test_dir = '/tmp/test_fs'
        os.mkdir(cls.test_dir)
        with open(os.path.join(cls.test_dir, 'file1.txt'), 'w') as f:
            f.write('This is file 1.\n')
        with open(os.path.join(cls.test_dir, 'file2.txt'), 'w') as f:
            f.write('This is file 2.\n')
        with tarfile.open(cls.test_tar, 'w') as tar:
            tar.add(cls.test_dir, arcname=os.path.basename(cls.test_dir))

        cls.emulator = Emulator('config.xml')
        cls.emulator.fs_path = cls.test_tar
        cls.emulator.load_virtual_fs()
        cls.emulator.current_dir = cls.emulator.virtual_fs

    @classmethod
    def tearDownClass(cls):
        # Удаление тестовых данных
        os.remove(cls.test_tar)
        os.rmdir(cls.test_dir)
        
    def test_ls(self):
        expected_files = ['file1.txt', 'file2.txt']
        result = self.emulator.ls()
        self.assertTrue(set(expected_files).issubset(set(result)))
    
    def test_cd_valid(self):
        self.emulator.cd('test_fs')
        self.assertEqual(self.emulator.current_dir, os.path.join(self.emulator.virtual_fs, 'test_fs'))

    def test_cd_invalid(self):
        result = self.emulator.cd('invalid_dir')
        self.assertEqual(result, "Directory not found.")
    
    def test_exit(self):
        result = self.emulator.exit()
        self.assertFalse(result)

    def test_chmod(self):
        result = self.emulator.chmod('755', 'file1.txt')
        self.assertEqual(result, "Changed mode of file1.txt to 755")

    def test_date(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = self.emulator.date()
        self.assertEqual(result, current_date)

