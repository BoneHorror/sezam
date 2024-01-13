import os
import subprocess

def internal_run(args: list, is64: bool):
    SAMASE = "bin\\samase.exe"
    SAMASE64 = "bin\\samase64.exe"

    path = [SAMASE if not is64 else SAMASE64, *args]
    print(f"Samase string debug: {path}")
    subprocess.run(path)

def run(path: str, is64: bool):
    internal_run([path], is64)

def build(path: str, is64: bool):
    internal_run([path, "--pack", os.getcwd() + "\\packed.exe"], is64)

def unpack(path: str, is64: bool):
    internal_run([os.getcwd() + "\\target\\", "--unpack", path], is64)
