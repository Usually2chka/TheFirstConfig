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

