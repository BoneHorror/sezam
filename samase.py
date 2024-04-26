import os
from shutil import rmtree
import subprocess
from utilities import log_print
from time import sleep

UNPK_TARGET = "\\target\\"
OS_TARGET = "target/"
def internal_run(args: list, is64: bool):
    SAMASE = "bin\\samase.exe"
    SAMASE64 = "bin\\samase64.exe"

    path = [SAMASE if not is64 else SAMASE64, *args]
    log_print(f"Samase string debug: {path}")
    subprocess.run(path)

def run(path: str, is64: bool):
    internal_run([path], is64)

def build(path: str, is64: bool):
    internal_run([path, "--pack", os.getcwd() + "\\packed.exe"], is64)

def unpack(path: str, is64: bool):
    try:
        if os.path.exists(OS_TARGET):
            log_print(f"\033[0;31mRemoving {os.path.abspath(OS_TARGET)} in 3 seconds... \033[0;32mCtrl+C\033[0;31m if not intended!\033[0;0m")
            sleep(3)
            rmtree(OS_TARGET)
            sleep(1)
            os.mkdir(OS_TARGET)
        internal_run([os.getcwd() + UNPK_TARGET, "--unpack", path], is64)
    except KeyboardInterrupt:
        log_print("\033[0;33mInterrupting unpack due to User input\033[0;0m")
