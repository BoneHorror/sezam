import os
import subprocess
import enum

SAMASE = "bin\\samase.exe"
SAMASE64 = "bin\\samase64.exe"

class OpType(enum.Enum):
    Run = enum.auto(), # ex: samase.exe C:\samase\uedaip
    Build = enum.auto(), # ex: samase.exe C:\samase\uedaip --pack C:\samase\UEDAIP_BroodWar.exe --pack_version "23.2212" --pack_icon uedr.ico
    Unpack = enum.auto(), # ex: samase.exe C:\samase\unpack --unpack C:\samase\unpack.exe

def samase_line_constructor(operation_type: OpType, path:str, is64: bool = False):
    local_samase = SAMASE if not is64 else SAMASE64
    match operation_type:
        case OpType.Run:
            return [local_samase, path]
        case OpType.Build:
            return [local_samase, path, "--pack", os.getcwd()+"\\packed.exe"]
        case OpType.Unpack:
            os.chdir("target")
            t_dir = os.getcwd()
            os.chdir("..")
            return [local_samase, t_dir, "--unpack", path]

class Samase:
    def __init__(self, folder: str = None, operation_type: OpType = None, is64: bool = False):
        self.folder = folder
        self.operation_type = operation_type
        self.is64 = is64

    def operate(self):
        print(f"Samase string debug: {samase_line_constructor(self.operation_type, self.folder, self.is64)}")
        subprocess.run(samase_line_constructor(self.operation_type, self.folder, self.is64))
