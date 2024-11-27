import os

def run(emulator, args):
    if not args:
        return '/'
    
    new_dir = os.path.normpath(os.path.join(emulator.current_dir, args[0]))
    if new_dir not in emulator.fs:
        print(f"Directory not found: {new_dir}")
        return emulator.current_dir
    
    return new_dir