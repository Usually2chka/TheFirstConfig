def run(emulator, args):
    if len(args) != 2:
        print("Usage: chmod <mode> <file>")
        return
    
    mode, file = args
    if file not in emulator.fs:
        print(f"File not found: {file}")
        return
    
    emulator.fs[file].mode = int(mode, 8)
    print(f"Changed mode of {file} to {mode}")