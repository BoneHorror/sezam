import os
import subprocess

SAMASE = "samase.exe"
SAMASE64 = "samase64.exe"

def samase_line_constructor(operation_type:int, path:str, is64: bool = False):
    local_samase = SAMASE if not is64 else SAMASE64
    match operation_type:
        case 0:
            return [local_samase, path]
        case 1:
            return [local_samase, path, "--pack", os.getcwd()+"\\packed.exe"]
        case 2:
            os.chdir("target")
            t_dir = os.getcwd()
            os.chdir("..")
            return [local_samase, t_dir, "--unpack", path]
        
class Samase:
    OP_TYPES = {
        0: "run", #ex: samase.exe C:\samase\uedaip
        1: "build", #ex: samase.exe C:\samase\uedaip --pack C:\samase\UEDAIP_BroodWar.exe --pack_version "23.2212" --pack_icon uedr.ico
        2: "unpack" #ex: samase.exe C:\samase\unpack --unpack C:\samase\unpack.exe
    }
    def __init__(self, folder: str = None, operation_type: int = None, is64: bool = False):
        self.folder = folder
        self.operation_type = operation_type
        self.is64 = is64

    def operate(self):
        print(f"Samase string debug: {samase_line_constructor(self.operation_type, self.folder, self.is64)}")
        subprocess.run(samase_line_constructor(self.operation_type, self.folder, self.is64))
