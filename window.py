#python3.12 window.py
#pyinstaller --onefile window.py
#pyinstaller window.spec
import PySimpleGUI as gui
import logging
from samase import Samase, OpType
import os

LOGFILE = "sezam.log"

localSamase = None
unpackSamase = None

def assertSet(value: any) -> bool:
    if value is None:
        print("Attempted to perform an operation without a directory selected!")
        return False
    return True
    
# Log setup
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=LOGFILE, encoding='utf8', level = logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logging.FileHandler(LOGFILE, mode = "w")

# Window layout
layout = [[gui.Button("Select build directory"), gui.Text("Please select a path", key="curPath"), gui.Push(), gui.Checkbox("Run in x64", key="x64")],
          [gui.Push(), gui.Button("Launch"), gui.Button("Build From"), gui.Push()],
          [gui.Push()],
          [gui.Button("Select .exe to Unpack"), gui.Text("No exe selected", key="curExe")],
          [gui.Push(), gui.Button("Unpack from"), gui.Push()]
]

window = gui.Window("Sezam", layout, resizable=True)
while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED:
        break
    if event == "Select build directory":
        directory = gui.popup_get_folder('Select path', initial_folder=os.getcwd())
        if directory == "":
            print("Nothing selected")
            continue
        clean_dir = directory[(directory.rfind("/")+1):]
        window["curPath"].update(value=clean_dir)
        localSamase = Samase(directory, None)
    if event == "Select Executable to Unpack":
        directory = gui.popup_get_file('Select path', initial_folder=os.getcwd(), file_types=(("Executable files", "*.exe"),))
        if directory == "":
            print("Nothing selected")
            continue
        clean_dir = directory[(directory.rfind("/")+1):]
        window["curExe"].update(value=clean_dir)
        unpackSamase = Samase(directory, None)
    if event == "Launch":
        if not assertSet(localSamase):
            continue
        localSamase.operation_type = OpType.Run
        localSamase.is64 = values["x64"]
        localSamase.operate()
    if event == "Build From":
        if not assertSet(localSamase):
            continue
        localSamase.operation_type = OpType.Build
        localSamase.is64 = values["x64"]
        localSamase.operate()
    if event == "Unpack from":
        if not assertSet(unpackSamase):
            continue
        assert unpackSamase.folder.endswith(".exe"), f"Expected executable to unpack, instead got {localSamase.folder}"
        unpackSamase.operation_type = OpType.Unpack
        localSamase.is64 = values["x64"]
        unpackSamase.operate()

    