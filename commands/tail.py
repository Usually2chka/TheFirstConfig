def run(emulator, args):
    if len(args) != 1:
        print("Usage: tail <file>")
        return
    
    file = args[0]
    if file not in emulator.fs:
        print(f"File not found: {file}")
        return
    
    with tarfile.open(emulator.fs_path, 'r') as tar:
        content = tar.extractfile(emulator.fs[file]).read().decode('utf-8')
    
    lines = content.splitlines()
    return '\n'.join(lines[-10:])