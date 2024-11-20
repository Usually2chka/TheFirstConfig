import os
import xml.etree.ElementTree as ET
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

if __name__ == "__main__":
    emulator = ShellEmulator('config.xml')
    emulator.run()
