import os
import tarfile
import xml.etree.ElementTree as ET
import datetime

class Emulator:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.current_dir = '/'
        self.virtual_fs = self.load_virtual_fs()

    def load_config(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()
        self.computer_name = root.find('computer_name').text
        self.fs_path = root.find('fs_path').text

    def load_virtual_fs(self):
        with tarfile.open(self.fs_path, 'r') as tar:
            tar.extractall(path='/tmp/virtual_fs')
        return '/tmp/virtual_fs'

    def ls(self):
        return os.listdir(self.current_dir)

    def cd(self, path):
        new_path = os.path.join(self.current_dir, path)
        if os.path.isdir(new_path):
            self.current_dir = new_path
        else:
            return "Directory not found."

    def exit(self):
        print("Exiting emulator...")
        return False

    def chmod(self, mode, file):
        # Псевдокод, так как chmod требует прав доступа
        return f"Changed mode of {file} to {mode}"

    def date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def tail(self, file, lines=10):
        try:
            with open(os.path.join(self.current_dir, file)) as f:
                return ''.join(f.readlines()[-lines:])
        except FileNotFoundError:
            return "File not found."

    def run(self):
        print(f"{self.computer_name} Emulator")
        while True:
            command = input(f"{self.computer_name}:{self.current_dir} $ ")
            cmd_parts = command.split()
            cmd = cmd_parts[0]

            if cmd == "ls":
                print(self.ls())
            elif cmd == "cd":
                if len(cmd_parts) > 1:
                    self.cd(cmd_parts[1])
                else:
                    print("No path specified.")
            elif cmd == "exit":
                if not self.exit():
                    break
            elif cmd == "chmod":
                if len(cmd_parts) == 3:
                    print(self.chmod(cmd_parts[1], cmd_parts[2]))
                else:
                    print("Usage: chmod <mode> <file>")
            elif cmd == "date":
                print(self.date())
            elif cmd == "tail":
                if len(cmd_parts) > 1:
                    print(self.tail(cmd_parts[1]))
                else:
                    print("No file specified.")
            else:
                print("Command not found.")



if __name__ == "__main__":
    emulator = Emulator('config.xml')
    emulator.run()