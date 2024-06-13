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
    current_samase = SAMASE if not is64 else SAMASE64
    log_print(f"Samase string debug: {path}")
    try:
        subprocess.run(path)
    except OSError as os_e:
        log_print(f"\033[0;31mOS Error when trying to run samase: \033[0;33m{os_e}\033[0;0m\nAre you sure samase executable is located in {current_samase}?")
    except Exception as err:
        log_print(f"\033[0;31mEncountered an exception when trying to run samase: \033[0;33m{err}\033[0;0m")

def run(path: str, is64: bool):
    internal_run([path], is64)

def build(path: str, is64: bool):
    internal_run([path, "--pack", os.getcwd() + "\\packed.exe"], is64)

def unpack(path: str, is64: bool, first_dir: str):
    try:
        if os.path.exists(OS_TARGET):
            log_print(f"\033[0;31mRemoving {os.path.abspath(OS_TARGET)} in 3 seconds... \033[0;32mCtrl+C\033[0;31m if not intended!\033[0;0m")
            sleep(3)
            rmtree(OS_TARGET)
            sleep(3)
            os.mkdir(OS_TARGET)
        internal_run([first_dir + UNPK_TARGET, "--unpack", path], is64)
    except KeyboardInterrupt:
        log_print("\033[0;33mInterrupting unpack due to User input\033[0;0m")
