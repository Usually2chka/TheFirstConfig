import xml.etree.ElementTree as ET
import tarfile
import os
import sys
from commands import chmod, date, tail, ls, cd, exit

class Emulator:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.hostname = self.config['hostname']
        self.fs_path = self.config['fs_path']
        self.current_dir = '/'
        self.fs = self.load_filesystem()

    def load_config(self, config_path):
        tree = ET.parse(config_path)
        root = tree.getroot()
        return {
            'hostname': root.find('hostname').text,
            'fs_path': root.find('fs_path').text
        }

    def load_filesystem(self):
        with tarfile.open(self.fs_path, 'r') as tar:
            return {member.name: member for member in tar.getmembers()}

    def run(self):
        while True:
            command = input(f"{self.hostname}:{self.current_dir}$ ")
            parts = command.split()
            if not parts:
                continue
            cmd, args = parts[0], parts[1:]
            
            if cmd == 'exit':
                exit.run(self, args)
                break
            elif cmd == 'cd':
                self.current_dir = cd.run(self, args)
            elif cmd == 'ls':
                print(ls.run(self, args))
            elif cmd == 'chmod':
                chmod.run(self, args)
            elif cmd == 'date':
                print(date.run(self, args))
            elif cmd == 'tail':
                print(tail.run(self, args))
            else:
                print(f"Command not found: {cmd}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python emulator.py <config_file>")
        sys.exit(1)
    
    emulator = Emulator(sys.argv[1])
    emulator.run()