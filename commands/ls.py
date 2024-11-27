def run(emulator, args):
    path = emulator.current_dir if not args else args[0]
    files = [name for name in emulator.fs.keys() if name.startswith(path)]
    return ' '.join(files)